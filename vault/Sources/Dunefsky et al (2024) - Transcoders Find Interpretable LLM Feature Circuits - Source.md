---
title: "Transcoders Find Interpretable LLM Feature Circuits - Source"
type: "source"
source_type: "pdf_text"
added: "2026-02-27"
---

Transcoders Find Interpretable LLM Feature Circuits
JacobDunefsky∗ PhilippeChlenski∗
YaleUniversity ColumbiaUniversity
NewHaven,CT06511 NewYork,NY10027
jacob.dunefsky@yale.edu pac@cs.columbia.edu
NeelNanda
Abstract
Akeygoalinmechanisticinterpretabilityiscircuitanalysis: findingsparsesub-
graphsofmodelscorrespondingtospecificbehaviorsorcapabilities. However,
MLPsublayersmakefine-grainedcircuitanalysisontransformer-basedlanguage
models difficult. In particular, interpretable features—such as those found by
sparseautoencoders(SAEs)—aretypicallylinearcombinationsofextremelymany
neurons, each with its own nonlinearity to account for. Circuit analysis in this
settingthuseitheryieldsintractablylargecircuitsorfailstodisentanglelocaland
globalbehavior. Toaddressthisweexploretranscoders,whichseektofaithfully
approximateadenselyactivatingMLPlayerwithawider,sparsely-activatingMLP
layer. Weintroduceanovelmethodforusingtranscoderstoperformweights-based
circuitanalysisthroughMLPsublayers. Theresultingcircuitsneatlyfactorizeinto
input-dependentandinput-invariantterms. Wethensuccessfullytraintranscoders
on language models with 120M, 410M, and 1.4B parameters, and find them to
performatleastonparwithSAEsintermsofsparsity,faithfulness,andhuman-
interpretability. Finally,weapplytranscoderstoreverse-engineerunknowncircuits
inthemodel,andweobtainnovelinsightsregardingthe“greater-thancircuit”in
GPT2-small. Ourresultssuggestthattranscoderscanproveeffectiveindecompos-
ingmodelcomputationsinvolvingMLPsintointerpretablecircuits. Codeisavail-
ableathttps://github.com/jacobdunefsky/transcoder_circuits/.
1 Introduction
Inrecentyears,transformer-basedlargelanguagemodels(LLMs)havedisplayedoutstandingperfor-
manceonawidevarietyoftasks[8,43,46].However,themechanismsbywhichLLMsperformthese
tasksareopaquebydefault[10,33]. Thefieldofmechanisticinterpretablity[9]seekstounderstand
these mechanisms, and doing so relies on decomposing a model into circuits [41]: interpretable
subcomputationsresponsibleforspecificmodelbehaviors[15,32,42,50].
Acoreprobleminfine-grainedcircuitanalysisisincorporatingMLPsublayers[32,38].Attemptingto
analyzeMLPneuronsdirectlysuffersfrom“polysemanticity”[3,16,24,40]:thetendencyofneurons
toactivateonmanyunrelatedconcepts. Toaddressthis,sparseautoencoders(SAEs)[7,12,51]
havebeenusedtoperformfine-grainedcircuitanalysisbyinsteadlookingatfeatures—vectorsinthe
model’srepresentationspace—insteadofindividualneurons[14,34]. However,whileSAEfeatures
areofteninterpretable, these vectorstendtobedenselinearcombinationsofmanyneurons[36].
Thus,mechanisticallyunderstandinghowanSAEfeaturebeforeoneormoreMLPlayersaffectsa
laterSAEfeaturemayrequireconsideringaninfeasiblenumberofneuronsandtheirnonlinearities.
Prior attempts to circumvent this [14, 34] use a mix of causal interventions and gradient-based
∗Equalcontribution.
38thConferenceonNeuralInformationProcessingSystems(NeurIPS2024).
4202
voN
6
]GL.sc[
2v44911.6042:viXra

Transformerlayer(×n )
L
Embedding + + Unembed
Attention MLPinput Transcoder MLPoutput SAE
W in Activation W out MLP
Figure1: AcomparisonbetweenSAEs,MLPtranscoders,andMLPsublayersforatransformer-
basedlanguagemodel. SAEslearntoreconstructmodelactivations,whereastranscodersimitate
sublayers’input-outputbehavior.
approximationstoMLPlayers.Buttheseapproachesfailtoexhibitinput-invariance:theconnections
betweenfeaturescanonlyeverbedescribedforagiveninput, andnotforthemodelasawhole.
Attemptstoaddressthis,e.g. byaveragingresultsovermanyinputs,converselylosetheirabilityto
yieldinput-dependentinformationthatdescribesaconnection’simportanceonasingleinput. This
meansthatSAEscannottellusaboutthegeneralinput-outputbehaviorofanMLPacrossallinputs.
Toaddresswhyinput-invarianceisdesirable,considerthefollowingexample: saythatonehasa
post-MLPSAEfeatureandwantstoseehowitiscomputedfrompre-MLPSAEfeatures. Doinge.g.
patchingononeinputshowsthatapre-MLPfeatureforPolishlastnamesisimportantforcausing
thepost-MLPfeaturetoactivate. Butonotherinputs,wouldfeaturesotherthanthePolishlastname
featurealsocausethepost-MLPfeaturetofire(e.g. anEnglishlastnamesfeature)? Couldtherebe
otherinputswherethePolishlastnamesfeaturefiresbutthepost-MLPfeaturedoesnot? Wecansee
thatwithoutinput-invariance,itisdifficulttomakegeneralclaimsaboutmodelbehavior.
Motivated by this, in this work, we explore transcoders (an idea proposed, but not explored,
inTempletonetal.[47]andLietal.[31]): wide,sparsely-activatingapproximationsofamodel’s
originalMLPsublayer. Specifically,MLPtranscodersarewideReLUMLPswithonehiddenlayer
that are trained to faithfully approximate the original narrower MLP sublayer’s output, with an
L1 regularization penalty on neuron activations to encourage sparse activations. Our primary
motivationistoenableinput-invariantfeature-levelcircuitanalysisthroughMLPsublayers,which
allowsustounderstandandinterpretthegeneralbehaviorofcircuitsinvolvingMLPsublayers.
Ourcontributions. Ourmaincontributionsare(1)tointroduceamethodforcircuitanalysisusing
transcoders,(2)toconfirmthattranscodersareafaithfulandinterpretableapproximationtoMLP
sublayers,and(3)todemonstratetheutilityofourcircuitanalysismethodondetailedcasestudies.
After describing the architecture of transcoders in §3.1, we demonstrate in §3.2 that transcoders
additionallyenablecircuit-findingtechniquesthatarenotpossibleusingSAEs,andintroduceanovel
methodforperformingcircuitanalysiswithtranscodersanddemonstratethattranscoderscleanly
factorizecircuitsintoinput-invariantandinput-dependentcomponents.
Then,in§4,weevaluatetranscoders’interpretability,sparsity,andfaithfulnesstotheoriginalmodel.
BecauseSAEsarethestandardmethodforfindingsparsedecompositionsofmodelactivations,we
comparetranscoderstoSAEsonmodelsupto1.4billionparametersandverifythattranscodersare
onparwithSAEsorbetterwithrespecttotheseproperties.
We apply transcoder circuit analysis to a variety of tasks in §5.1 and §5.2, including “blind case
studies,” whichdemonstratehowthisapproachallowsustounderstandfeatureswithoutlooking
atspecificexamples,andanin-depthanalysisoftheGPT2-small“greater-thancircuit”previously
studiedbyHannaetal.[26].
2 Transformerspreliminaries
FollowingElhageetal.[15],werepresentthecomputationofatransformermodelasfollows. First,
themodelmapsinputtokens(andtheirpositions)toembeddingsx(
p
0
r
,
e
t) ∈Rdmodel,wheretisthetoken
indexandd isthemodeldimensionality. Then,themodelappliesaseriesof“layers,”whichmap
model
thehiddenstateattheendofthepreviousblocktothenewhiddenstate. Thiscanbeexpressedas:
2

x(l,t) =x(l,t)+ (cid:88) attn(l,h) (cid:16) x(l,t);x(l,1:t) (cid:17) (1)
mid pre pre pre
headh
(cid:16) (cid:17)
x(l+1,t) =x(l,t) +MLP(l) x(l,t) (2)
pre mid mid
where l is the layer index, t is the token index, attn(l,h)(x(l,t);x(l,1:t)) denotes the output of
pre pre
attentionheadhatlayerlgivenallprecedingsourcetokensx(l,1:t)anddestinationtokenx(l,t),and
pre pre
MLP(l)(x(l,t))denotestheoutputofthelayerlMLP.2
mid
Equation1showshowtheattentionsublayerupdatesthehiddenstateattokent,andEquation2
showshowtheMLPsublayerupdatesthehiddenstate. Importantly,eachsublayeralwaysaddsits
outputtothecurrenthiddenstate. Assuch,thehiddenstatealwayscanbeadditivelydecomposed
intotheoutputsofallprevioussublayers. ThismotivatesElhageetal.[15]torefertoeachtoken’s
hiddenstateasitsresidualstream,whichis“readfrom”and“writtento”byeachsublayer.
3 Transcoders
3.1 Architectureandtraining
Transcodersaimtolearna“sparsified”approximationofanMLPsublayer: theyapproximatethe
outputofanMLPsublayerasasparselinearcombinationoffeaturevectors. Formally,thetranscoder
architecturecanbeexpressedas
z (x)=ReLU(W x+b ) (3)
TC enc enc
TC(x)=W z (x)+b , (4)
dec TC dec
wherexistheinputtotheMLPsublayer,W
enc
∈ Rdfeatures×dmodel,W
dec
∈ Rdmodel×dfeatures,b
enc
∈
Rdfeatures,b
dec
∈ Rdmodel,d
features
isthenumberoffeaturevectorsinthetranscoder,andd
model
isthe
dimensionalityoftheMLPinputactivations. Usually,d isfargreaterthand .
features model
Eachfeatureinatranscoderisassociatedwithtwovectors: thei-throwofW istheencoder
enc
featurevectoroffeaturei,andthei-thcolumnofW isthedecoderfeaturevectoroffeature
dec
i. Thei-thcomponentofz (x)iscalledtheactivationoffeaturei. Intuitively,foreachfeature,
TC
theencodervectorisusedtodeterminehowmuchthefeatureshouldactivate;thedecodervectoris
thenscaledbythisamount,andtheresultingweightedsumofdecodervectorsistheoutputofthe
transcoder. Inthispaper,thenotationf(l,i)andf(l,i)isusedtodenotethei-thencoderfeaturevector
enc dec
anddecoderfeaturevector,respectively,inthelayerltranscoder.
BecausewewanttranscoderstolearntoapproximateanMLPsublayer’scomputationwithasparse
linearcombinationoffeaturevectors,transcodersaretrainedwiththefollowingloss,whereλ isa
1
hyperparametermediatingthetradeoffbetweensparsityandfaithfulness:
L (x)=∥MLP(x)−TC(x)∥2+λ ∥z (x)∥ . (5)
TC 2 1 TC 1
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
faithfulnessloss sparsitypenalty
3.2 Circuitanalysiswithtranscoders
We now introduce a novel method for performing feature-level circuit analysis with transcoders,
whichprovidesascalableandinterpretablewaytoidentifywhichtranscoderfeaturesindifferent
layersconnecttocomputeagiventask. Importantly,thismethodprovidesinsightsintothegeneral
input-outputbehaviorofMLPsublayers,whichSAE-basedmethodscannotdo.
Inparticular,theprimarygoalofcircuitanalysisistoidentifyasubgraphofthemodel’scomputational
graphthatisresponsiblefor(mostof)themodel’sbehavioronagiventask[11,19,20];thisrequires
ameansofevaluatingacomputationalsubgraph’simportancetothetaskinquestion. Inorderto
2Notethatthe“Pythia”familyofmodelscomputesMLPandattentionsublayeroutputsinparallel. This
(cid:16) (cid:17)
meansthatEquation2isthusgivenbyx(l+1,t) =x(l,t)+MLP(l) x(l,t) .
pre mid pre
3

Feature
Feature Feature Feature
Feature
Step1: findthedirect
contributionsofearlier-
layerfeaturestoalater-
layerfeature. Feature Feature Feature
Feature
Step 2: delete all but Step3: selectthetop- Step4:deleteallbutthe Step5:Repeatsteps2– Step 6: Merge top k
the k most highly- contributingfeaturesfor kmostimportantpaths 4untilyouhavepathsof paths into a single cir-
contributingfeatures. eachselectedfeatures. inthegraphagain. lengthl. cuit.
Figure2: Avisualizationofthecircuit-findingalgorithm.
determine which edges are included in this subgraph, we thus have to compute attributions for
each edge: how much the earlier node contributes to the later node’s own contribution. Circuit
analysiswithSAEsthusentailscomputingtheattributionofpre-MLPSAEfeaturestopost-MLP
SAEfeatures,asmediatedthroughtheMLP.Standardmethodsforcomputingattributionsarecausal
patching(whichinherentlyonlygivesinformationaboutlocalMLPbehavioronasingleinput)and
methodslikeinput-times-gradientorattributionpatching(whichareequivalentinthissetting). We
willnowdemonstratewhythesemethodscannotyieldinformationabouttheMLP’sgeneralbehavior.
Lettingzbetheactivationofanearlier-layerfeature,z′ betheactivationofthelater-layerfeature,
andybetheactivationoftheMLPatlayerl′,theinput-times-gradientisgivenby:
(cid:18) ∂z′(cid:19) (cid:18) ∂z′∂y (cid:19)
z =z . (6)
∂z ∂y ∂z
Unfortunately,notonlyiszinput-dependent,butsois ∂z′ aswell,because ∂y is.
∂z ∂z
ThismeansthatwecannotuseSAEstounderstandthegeneralbehaviorofMLPsonvariousinputs.In
contrast,wewillshowthatwhenwereplaceMLPsublayerswithsufficientlyfaithfulandinterpretable
transcoders,weobtainattributionsthatneatlyfactorizeintoinput-dependenttermsandinput-invariant
terms;thelattercanbecomputedjustfrommodelandtranscoderweights,andtellusabouttheMLP
behavioracrossallinputs.
3.2.1 Attributionbetweentranscoderfeaturepairs
We begin by showing how to compute attributions between pairs of transcoder features. This
attributionisgivenbytheproductoftwoterms: theearlierfeature’sactivation(whichdependsonthe
inputtothemodel),andthedotproductoftheearlierfeature’sdecodervectorwiththelaterfeature’s
encodervector(whichisindependentofthemodelinput).
(cid:16) (cid:17)
Thefollowingisamoreformalrestatement. Letz(l,i) x(l,t) denotethescalaractivationofthei-th
TC mid
featureinthelayerltranscoderontokent,asafunctionoftheMLPinputx(l,t) attokentinlayer
mid
l. Thenforlayerl<l′,thecontributionoffeatureiintranscoderltotheactivationoffeaturei′in
transcoderl′ontokentisgivenby
(cid:16) (cid:17)(cid:16) (cid:17)
z(l,i) x(l,t) f(l,i)·f(l′,i′) (7)
TC mid dec enc
(cid:124) (cid:123)(cid:122) (cid:125)(cid:124) (cid:123)(cid:122) (cid:125)
input-dependent input-invariant
This expression is derived in App. D.2. Note that
(cid:16) f(l,i)·f(l′,i′) (cid:17)
is input-invariant: once the
dec enc
transcoders have been trained, this term does not depend on the input to the model. This term,
4

analyzedinisolation,canthusbeviewedasprovidinginformationaboutthegeneralbehaviorof
(cid:16) (cid:17)
themodel. Theonlyinput-dependenttermisz(l,i) x(l,t) ,theactivationoffeatureiinthelayerl
TC mid
transcoderontokent. Assuch,thisexpressioncleanlyfactorizesintoatermreflectingthegeneral
input-invariant connection between the pair of features and an interpretable term reflecting the
importanceoftheearlierfeatureonthecurrentinput.
3.2.2 Attributionthroughattentionheads
Sofar,wehaveaddressedhowtofindtheattributionofalower-layertranscoderfeaturedirectlyon
ahigher-layertranscoderfeatureatthesametoken. Buttranscoderfeaturescanalsobemediated
byattentionheads. Wewillthusextendtheaboveanalysistoaccountforfindingtheattributionof
transcoderfeaturesthroughtheOVcircuitofanattentionhead. Forafullderivation,seeApp. D.3.
Asbefore,wewanttounderstandwhatcausesfeaturei′inthelayerl′transcodertoactivateontoken
t. Givenattentionheadhatlayerlwithl<l′,thecontributionoftokensatlayerlthroughheadh
tofeaturei′inlayerl′attokentisgivenby
(cid:16) (cid:17)(cid:18)(cid:18)(cid:16) (cid:17)T (cid:19) (cid:19)
score(l,h) x(l,t),x(l,s) W(l,h) f(l′,i′) ·x(l,s) , (8)
pre pre OV enc pre
(cid:16) (cid:17)
wherescore(l,h) x(l,t),x(l,s) istheattentionscoreforheadhandlayerlfromtokenstotokent.
pre pre
3.2.3 Findingcomputationalsubgraphs
Usingthisobservation,wepresentamethodforfindingcomputationalsubgraphs. Wenowknow
howtodetermine,onagiveninputandtranscoderfeaturei′,whichearlier-layertranscoderfeaturesi
areimportantforcausingi′toactivate. Oncewehaveidentifiedsomeearlier-layerfeaturesithatare
relevanttoi′,thenwecanthenrecurseonitounderstandthemostimportantfeaturescausingito
activatebyrepeatingthisprocess.
Doingsoiteratively(andgreedilypruningallbutthemostimportantfeaturesateachstep)thusyields
asetofcomputationalpaths(asequenceofconnectededges). Thesecomputationalpathscanthen
becombinedintoacomputationalsubgraph, insuchawaythateachnode(transcoderfeatureor
attentionhead),edge,andpathisassignedanattribution. Afulldescriptionofthecircuit-finding
algorithmispresentedinApp. D.5. Figure2providesavisualizationofthisalgorithm.
3.2.4 De-embeddings: aspecialcaseofinput-invariantinformation
Earlier,wediscussedhowtocomputetheinput-invariantconnectionbetweenapairoftranscoder
features,providinginsightsongeneralbehaviorofthemodel. Arelatedtechniqueissomethingthat
wecallde-embeddings. Ade-embeddingvectorforatranscoderfeatureisavectorthatcontainsthe
directeffectoftheembeddingofeachtokeninthemodel’svocabularyonthetranscoderfeature. The
de-embeddingvectorforfeatureiinthelayerltranscoderisgivenbyW Tf(l,i),whereW isthe
E enc E
model’stokenembeddingmatrix. Importantly,thisvectorgivesusinput-invariantinformationabout
howmucheachpossibleinputtokenwoulddirectlycontributetothefeature’sactivation.
Givenade-embeddingvector,lookingatwhichtokensinthemodel’svocabularyhavethehighestde-
embeddingscorestellsusaboutthefeature’sgeneralbehavior. Forexample,foracertainGPT2-small
MLP0transcoderfeaturethatweinvestigated,thetokenswiththehighestscoreswereoglu,owsky,
zyk,chenko,andkowski. Noticetheinterpretablepattern: allofthesetokenscomefromEuropean
surnames,primarilyPolishones,suggestingthatthefeaturegenerallyfiresonPolishsurnames.
4 ComparisonwithSAEs
TranscoderswereoriginallyconceivedasavariantofSAEs,andassuch,therearemanysimilarities
between them. They differ only in their training objective: because SAEs are autoencoders, the
faithfulnesstermintheSAElossmeasuresthereconstructionerrorbetweentheSAE’soutputandits
originalinput. Incontrast,thefaithfulnesstermofthetranscoderlossmeasurestheerrorbetweenthe
transcoder’soutputandtheoriginalMLPsublayer’soutput.
5

Table1: Thenumberofinterpretablefeatures,possibly-interpretablefeatures,anduninterpretable
featuresforthetranscoderandMLP-inSAE.Oftheinterpretablefeatures,weadditionallydeemed6
transcoderfeatures,and16SAEfeaturestobe“context-free”,meaningtheyappearedtofireona
singletokenwithoutanyevidentcontext-dependentpatterns.
Transcoder MLP-inSAE
#interpretable 41 38
#maybe 8 8
#uninterpretable 1 4
Becauseofthesesimilarities,SAEscanbequantitativelyevaluated(forsparsityandfidelity)and
qualitativelyevaluated(forfeatureinterpretability)inpreciselythesamewayastranscoders,using
standardSAEevaluationmethods [4,29]. WenowreporttheresultsofevaluationscomparingSAEs
totranscodersonthesemetrics,andfindthattranscodersarecomparabletoorbetterthanSAEs.
4.1 BlindinterpretabilitycomparisonoftranscoderstoSAEs
Inordertoevaluatetheinterpretabilityoftranscoders,wemanuallyattemptedtointerpret50random
featuresfromaPythia-410Mlayer15transcoderand50randomfeaturesfromaPythia-410Mlayer15
SAEtrainedonMLPinputs.3 Foreachfeature,theexamplesinasubsetoftheOpenWebTextcorpus
thatcausedthefeaturetoactivatethemostwerecomputedaheadoftime. Then,thefeaturesfrom
boththeSAEandthetranscoderwererandomlyshuffled. Foreachfeature,themaximum-activating
examplesweredisplayed,butnotwhetherthefeaturecamefromanSAEortranscoder. Werecorded
foreachfeaturewhetherornotthereseemedtobeaninterpretablepattern,andonlyafterexamining
everyfeaturedidwelookatwhichfeaturescamefromwhere. Theresults,showninTable1,suggest
transcoderfeaturesareapproximatelyasinterpretableasSAEfeatures. Thisfurthersuggeststhat
transcodersincurnopenaltiescomparedtoSAEs.
4.2 QuantitativecomparisonoftranscoderstoSAEs
4.2.1 Evaluationmetrics
Weevaulatetranscodersqualitativelyontheirfeatures’interpretabilityasjudgedbyahumanrater,and
quantitativelyonthesparsityoftheiractivationsandtheirfidelitytotheoriginalMLP’scomputation.
Asaqualitativeproxymeasurefortheinterpretabilityofafeature,wefollowBrickenetal.[7]in
assumingthatinterpretablefeaturesshoulddemonstrateinterpretablepatternsintheexamplesthat
causethemtoactivate. Tothisend,onecanrunthetranscoderonalargedatasetoftext,seewhich
datasetexamplescausethefeaturetoactivate,andseeifthereisaninterpretablepatternamongthese
tokens. Whileimperfect[6],thisisstillareasonableproxyforaninherentlyqualitativeconcept.
Tomeasurethesparsityofatranscoder,onecanrunthetranscoderonadatasetofinputs,andcalculate
themeannumberoffeaturesactiveoneachtoken(themeanL normoftheactivations). Tomeasure
0
thefidelityofthetranscoder,onecanperformthefollowingprocedure. First,runtheoriginalmodel
onalargedatasetofinputs,andmeasurethenext-token-predictioncrossentropylossonthedataset.
Then,replacethemodel’sMLPsublayercorrespondingtothetranscoderwiththetranscoder,and
measurethemodifiedmodel’smeanlossonthedataset. Now,thefaithfulnessofthetranscodercan
bequantifiedasthedifferencebetweenthemodifiedmodel’slossandtheoriginalmodel’sloss.
4.2.2 Results
WetrainedSAEsandtranscodersonactivationsfromGPT2-small[44],Pythia-410M,andPythia-
1.4B[2]. Foreachmodel,wetrainedmultipleSAEsandtranscodersonthesameinputs,butwith
differentvaluesoftheλ hyperparametercontrollingthefidelity-sparsitytradeoffforeachSAEand
1
eachtranscoder. ThetranscodersweretrainedonMLP-inandMLP-outactivations,whileSAEswere
3WeusedSAEstrainedonMLPinputsherebecausetheinterpretabilitycasestudieslookatfeatureactivations,
whicharesolelydependentontheencodervectorsoftheSAEsandtranscoders.Becausetranscoders’encoder
vectorsliveinMLPinputspace,wethoughtthatthecomparisonwouldbemostaccurateifourSAEs’encoder
vectorsalsolivedinMLPinputspace.
6

3.60
3.62 3.64
3.66
3.68
0 20 40 60 80 100 120 140
Mean L0
ssol naeM
GPT2-small layer 8
3.32
1: 6.0E-05 1: 1.0E-04 1: 1.4 1 E : 1 -0 .2 4 E-0 1: 4 1.0E- 1 0 : 4 2. 1 0 : E 8 - . 0 0 4 E 1: - 0 1 5 .7E-04 1: 1.4E-04 1: 1.2E-04 3 3 . . 3 3 4 6 1: 1.7E-04 3.38
1: 2.10: E2-.054E-04
Transcoder 3.40
1: 2.5E-04 S O A ri E ginal model
Mean ablate MLP sublayer 3.42
0 50 100 150 200 250
Mean L0
ssol naeM
Pythia-410M layer 15
3.10
1: 5.5E-05 1: 4.0E-05 1: 3.0E-05 1: 2.0E-05 3 3 . . 1 1 1 2 1: 7.0E-05 1: 7.0E-05 1: 8.5E-05 3.13 1: 1.0E-04 3.14
3.15 Transcoder
S O A ri E ginal model 3.16
Mean ablate MLP sublayer 3.17
10 20 30 40 50 60 70
Mean L0
ssol naeM
Pythia-1.4B layer 15
1: 1.8E-05 1: 2.5E-05 1: 3.5E-05 1: 3.2E-05 1: 3.8E-05
1: 5.5E-05 T
S
r
A
a
E
nscoder
Original model
Mean ablate MLP sublayer
Figure3: Thesparsity-accuracytradeoffoftranscodersversusSAEsonGPT2-small,Pythia-410M,
andPythia-1.4B.EachpointcorrespondstoatrainedSAEortranscoder,andislabeledwiththeL1
regularizationpenaltyλ usedduringtraining.
1
trainedonMLP-outactivations(asthesearetheactivationsthatMLPSAEsaretypicallytrained
on). Due to compute limitations, we used the same learning rate, which was determined via a
hyperparametersweepontranscoders,forbothSAEsandtranscoders. Thismeansthatthelearning
ratemightnotbeoptimalforSAEs. Nevertheless,wedidperformaseparatehyperparametersweep
ofλ fortheSAEsandtranscoders.
1
WeevaluatedeachSAEandtranscoderonthesame3.2MtokensofOpenWebTextdata[21]. Wealso
recordedthelossoftheunmodifiedandmean-ablatedmodel(alwaysreplacingtheMLPsublayer
outputwithitsmeanoutputoverthedataset)asbest-andworst-casebounds,respectively.
WesummarizetheParetofrontiersofthesparsity-accuracytradeoffforallmodelsinFigure3. In
all cases, transcoders are equal to or better than SAEs. In fact, the gap between transcoders and
SAEsseemstowidenonlargermodels. Note,however,thatcomputelimitationspreventedusfrom
performingmoreexhaustivehyperparametersweeps;assuch,itmightbepossiblethatadifferentset
ofhyperparameterscouldhaveallowedSAEstosurpasstranscoders. Nonetheless,theseresultsmake
usoptimisticthatusingtranscodersincursnopenaltiesversusSAEstrainedonMLPactivations.
5 Circuitanalysiscasestudies
5.1 Blindcasestudy: reverse-engineeringafeature
Tounderstandtheutilityoftranscodersforcircuitanalysis,wecarriedoutnineblindcasestudies,
where we randomly selected individual transcoder features in a ninth-layer (of 12) GPT2-small
transcoderandusedcircuitanalysistoformahypothesisaboutthesemanticsofthefeature—without
lookingatthetextofexamplesthatcausethefeaturetoactivate. Inblindcasestudies, weusea
combinationofinput-invariantandinput-dependentinformationtoallowustoevaluatetranscoders
asatooltoinfermodelbehaviorwithminimalpromptinformation. Thisbetterreflectsakeygoalof
mechanisticinterpretability: tobeabletounderstandmodelbehavioronunknown,unforeseentasks.
Incontrast,reverse-engineeringafeaturewhereonealreadyhasanideaofitsbehaviorcanintroduce
confirmationbias. Forinstance,lookingatactivationpatternspriortocircuitanalysiscanpredispose
aresearchertoseekoutonlycircuitsthatcorroboratetheirinterpretationoftheseactivationpatterns,
potentiallyignoringcircuitsthatrevealotherinformationaboutthefeature. Conversely,ifthecircuit
analysismethodisfaultyandyieldssomeexplanationsthatarenotreflectedinthefeatureactivations,
then the researcher might ignore those spurious explanations and thus obtain an overly-positive
assessmentofthecircuitanalysismethod. The“rulesofthegame”forblindcasestudiesarethat:
1. Thespecifictokenscontainedinanypromptarenotallowedtobedirectlyseen. Assuch,prompts
andtokenscanonlybereferencedbytheirindexinthedataset.
2. Thesepromptsmaybeusedtocomputeinput-dependentinformation(activationsandcircuits),as
longasthetokensthemselvesremainhidden.
3. Anyinput-invariantinformation,includingfeaturede-embeddings,isallowed.
Inthissection,wesummariseaspecificblindcasestudy,howweusedourcircuitstoreverse-engineer
feature 355 in our layer 8 transcoder. Other studies, as well as a longer description of the study
summarizedhere,canbefoundinApp.H.
7

Notethatweusethefollowingcompactnotationfortranscoderfeatures: tcA[B]@Creferstofeature
BinthelayerAtranscoderattokenC.
Buildingthefirstcircuit. Westartedbygettingalistofindicesofthetop-activatingpromptsin
thedatasetfortc8[355]. Importantly, wedidnotlookattheactualtokensintheseprompts, as
doingsowouldviolateRule1. Forourfirstinput,wechoseexample5701,token37;tc8[355]fires
atstrength11.91onthistokeninthisinput. Ourgreedyalgorithmforfindingthemostimportant
computationalpathsforcausingtc8[355]@37tofirerevealedcontributionsfromthecurrenttoken
(37)andearliertokens(like35,36,and31).
Current-tokenfeatures. Fromtoken37,wefoundstrongcontributionsfromtc0[16632]@37and
tc0[9188]@37. Input-invariantde-embeddingsoftheselayer0featuresrevealedthattheyprimarily
activate on variants of;, suggesting that token 37 contributed to the feature by virtue of being a
semicolon. Another feature which contributed strongly through the current token, tc6[11831],
showedasimilarpattern. Amongthetopinput-invariantconnectionsfromlayer0transcoderfeatures
totc6[11831],weonceagainfoundthesamesemicolonfeaturestc0[16632]andtc0[9188].
Previous-token features. Next we checked computational paths from previous tokens through
attention heads. Looking at these contextual computational paths revealed a contribution from
tc0[13196]@36;thetopde-embeddingsforthisfeaturewereyearslike1973,1971,1967,and1966.
Additionally,therewasacontributionfromtc0[10109]@31,forwhichthetopde-embeddingwas(.
Furthermore,therewasacontributionfromtc6[21046]@35. Thetopinput-invariantconnectionsto
thisfeaturefromlayer0weretc0[16382]andtc0[5468]. Thetopde-embeddingsfortheformer
weretokensassociatedwithEasternEuropeanlastnames(e.g.kowski,chenko,owicz)andthetop
de-embeddingsforthelatterfeaturewereEnglishsurnames(e.g. Burnett, Hawkins, Johnston).
Thisheavilysuggestedthattc6[21046]wasasurnamefeature.
Thus,thecircuitrevealedthispatternwasimportanttoourfeature: “(-[?]-[?]-[?]-[surname]-[year]-;”.
Analysis. We hypothesized that tc8[355] fires on semicolons in parenthetical citations like
“(Vaswanietal. 2017;Elhageetal. 2021)”. Furtherinvestigationonanotherinputyieldedasimilar
pattern—alongwithafeaturewhosetopde-embeddingtokensincluded Accessed, Retrieved,
Neuroscience,and Springer. Thisbolsteredourhypothesisevenmore.
Here,wedecidedtoendtheblindcasestudyandcheckifourhypothesiswascorrect. Sureenough,
thetopactivatingexamplesincludedsemicolonsincitationssuchas“(Poeck,1969;Rinn,1984)”
and“(Robinsonetal.,1984;Starksteinetal.,1988)”. Wenotethatthefirstoftheseistheexampleat
index(5701,37)weanalyzedabove.
“Restricted” blind case studies. Because MLP0 features tend to be single-token, significant
informationabouttheoriginalpromptcanbeobtainedbylookingatwhichMLP0transcoderfeatures
areactiveandthentakingtheirde-embeddings. Inordertoaddressthisandmorefullyinvestigate
thepowerofinput-invariantcircuitanalysis,sixoftheeightcasestudiesthatwecarriedoutwere
restrictedblindcasestudies,inwhichallinput-dependentMLP0featureinformationisforbidden
touse. Formoredetailsonthesecasestudies,seeAppendixH.2.
5.2 AnalyzingtheGPT2-small“greater-than”circuit
Wenowturntoaddressthe“greater-than”circuitinGPT2-smallpreviouslyconsideredbyHanna
etal.[25]. Theyconsideredthefollowingquestion: givenapromptsuchas“Thewarlastedfrom
1737to17”,howdoesthemodelknowthatthepredictednextyeartokenhastobegreaterthan1737?
Intheiroriginalwork,theyanalyzedthecircuitresponsibleforthisbehavioranddemonstratedthat
MLP10playsanimportantrole,lookingintotheoperationofMLP10ataneuronallevel. Wenow
applytranscodersandthecircuitanalysistoolsaccompanyingthemtothissameproblem.
5.2.1 Initialinvestigation
First,weusedthemethodsfromSec.3.2.3toinvestigateasinglepromptandobtainthecomputational
pathsmostrelevanttothetask. ThisplacedahighattributiononMLP10features,whichwerein
turnactivatedbyearlier-layerfeaturesmediatedbyattentionhead1inlayer9. Thiscorroboratesthe
analysisintheoriginalwork.
8

0.85
0.80
0.75
0.70
0.65
0 10 20 30 40 50 60
Number of features/neurons
ecnereffid
ytilibaborP
Performance vs. # of features/neurons used
1.10
1.05
1.00
0.95
Original model 0.90
Replace with TC10 (without tc10[5315])
Transcoder features (without tc10[5315]) 0.85
Neurons
Replace with TC10 0.80 Transcoder features (with tc10[5315])
Remove MLP10 entirely
0.75
0 20 40 60 80 100
Year token
esaercni
tigoL
Logits boosted by transcoder feature 5315
Logit increase
Normalized de-embedding score
Figure4: Left: Performanceaccordingtotheprobabilitydifferencemetricwhenallbutthetopk
featuresorneuronsinMLP10arezero-ablated. Right: TheDLAandde-embeddingscorefor
tc10[5315],whichcontributednegativelytothetranscoder’sperformance.
Next,weinvestigatedwhichMLP10transcoderfeaturesweremostimportantonavarietyofprompts,
andhowtheiractivationsaremediatedbyattentionhead1inlayer9. Followingtheoriginalwork,we
generatedall100promptsoftheform“Thewarlastedfrom17YYto17”,whereYYdenotesatwo-digit
number. WefoundthattheMLP10featureswiththehighestvarianceinactivationsoverthissetof
promptsalsohadtopinput-dependentconnectionsfromMLP0featuresthroughattentionhead1in
layer9whosetopde-embeddingsweretwo-digitnumbers. Thetopinput-invariantconnectionsfrom
MLP0featuresthroughattentionhead1inlayer9toMLP10featuresalsohadtwo-digitnumbers
amongtheirtopde-embeddingtokens. Thispositiveresultwassomewhatunexpected,giventhat
thereareonly100two-digitnumbertokensinthemodel’svocabularyofover50ktokens.
Wethenuseddirectlogitattribution(DLA)[15]tolookattheeffectofeachtranscoderfeature
onthepredictedlogitsofeachYYtokeninthemodel’svocabulary. Theseresults, alongwithde-
embeddingscoresforeachYYtoken,canbeseeninFigure5. Thede-embeddingsscoresarehighest
forYYtokenswhereyearsfollowingthemareboostedandyearsprecedingthemareinhibited.
5.2.2 Comparisonwithneuronalapproach
Next,wecomparedthetranscoderapproachtotheneuronalapproachtoseewhethertranscoders
giveasparser descriptionofthecircuitthanMLPneuronsdo. Todothis, wecomputedthe100
highest-variance layer 10 transcoder features and MLP10 neurons. Then, for 1 ≤ k ≤ 100, we
zero-ablatedallbutthetopkfeaturesinthetranscoder/neuronsinMLP10andmeasuredhowthis
affectedthemodel’sperformanceaccordingtothemeanprobabilitydifferencemetricpresentedin
theoriginalpaper. Wealsoevaluatedtheoriginalmodelwithrespecttothismetric,alongwiththe
modelwhenMLP10isreplacedwiththefulltranscoder.
TheresultsareshowninthelefthalfofFigure4. Forfewerthan24features,thetranscoderapproach
outperforms the neuronal approach; its performance drops sharply, however, around this point.
Furtherinvestigationrevealedthattc10[5315],the24th-highest-variancetranscoderfeature,was
responsibleforthisdropinperformance. TheDLAforthisfeatureisplottedintherighthalfof
Figure4. Noticehow,incontrastwiththethreehighest-variancetranscoderfeatures,tc10[5315]
displaysaflatterDLA,boostingalltokensequally. Thismightexplainwhyitcontributestopoor
performance. Toaccountforthis,notethatthelefthalfofFigure4alsodemonstratestheperformance
ofthetranscoderwhenthis“badfeature”isremoved.
Whilethetranscoderdoesnotrecoverthefullperformanceoftheoriginalmodel,itneedsonlya
handfuloffeaturestorecovermostoftheoriginalmodel’sperformance;manymoreMLPneurons
areneededtoachievethesamelevelofperformance. Thissuggeststhatthetranscoderisparticularly
usefulforobtainingasparse,understandableapproximationofMLP10. Furthermore,thetranscoder
featuressuggestasimplewaythattheMLP10computationmay(approximately)happen: byasmall
setoffeaturesthatfireonyearsincertainrangesandboostthelogitsforthefollowingyears.
9

0.8
0.6
0.4
0.2
0.0
0.2
0.4
0.6
0 20 40 60 80 100
Year token
esaercni
tigoL
Logits boosted by transcoder feature 1954
Logit increase 0.8 Normalized de-embedding score
0.6
0.4
0.2
0.0
0.2
0 20 40 60 80 100
Year token
esaercni
tigoL
Logits boosted by transcoder feature 21238
0.6
0.4
0.2
0.0
0.2
L N o o g r i m t a in li c z r e e d a s d e e-embedding score 0.4
0 20 40 60 80 100
Year token
esaercni
tigoL
Logits boosted by transcoder feature 10437
Logit increase Normalized de-embedding score
Figure 5: For the three MLP10 transcoder features with the highest activation variance over the
“greater-than” dataset, and for every possible YY token, we plot the direct logit attribution (the
extenttowhichthefeaturebooststheoutputprobabilityofYY)andthede-embeddingscore(an
input-invariantmeasurementofhowmuchYYcausesthefeaturetofire).
6 Relatedwork
Circuit analysis is a common framework for exploring model internals [15, 32, 41]. A number
of approaches exist to find circuits and meaningful components in models, including causal ap-
proaches[20],automatedcircuitdiscovery[11],andsparseprobing[24]. Causalmethodsinclude
activation patching [28, 49, 52], attribution patching [30, 39], and path patching [22, 50]. Much
circuit analysis work has focused on attention head circuits [18], including copying heads [15],
inductionheads[42],copysuppression[35],andsuccessorheads[23]. Methodsconnectingcircuit
analysistoSAEsincludeHeetal.[27],Batsonetal.[1]andMarksetal.[34]. Ourrecursivegreedy
circuit-findingapproachwaslargelybasedonthatofDunefsky&Cohan[13].
Sparse autoencoders have been used to disentangle model activations into interpretable fea-
tures[7,12,51]. ThedevelopmentofSAEswasmotivatedbythetheoryofsuperpositioninneural
representations[17]. Sincethen,muchrecentworkhasfocusedonexploringandinterpretingSAEs,
andconnectingthemtopreexistingmechanisticinterpretabilitytechniques. Notablecontributions
includetoolsforexploringSAEfeatures,suchasSAElens[5];applicationsofSAEstoattention
sublayers [29]; scaling up SAEs to Claude 3 Sonnet [48] and improved SAE architectures [45].
TranscodershavebeenpreviouslyproposedasavariantofSAEsunderthenames“predictingfuture
activations” [47]and“MLPstretchers”[31],butnotexploredindetail.
7 Conclusion
Fine-grainedcircuitanalysisrequiresanapproachtohandlingMLPsublayers. Toourknowledge,
thetranscoder-basedcircuitanalysismethodpresentedhereistheonlysuchapproachthatcleanly
disentanglesinput-invariantinformationfrominput-dependentinformation. Importantly,transcoders
bring these benefits without sacrificing fidelity and interpretability: when compared to state-of-
the-artfeature-levelinterpretabilitytools(SAEs),wefindthattranscodersachieveequalorbetter
performance. Wethusbelievethattranscodersareanimprovementoverotherformsoffeature-level
interpretabilitytoolsforMLPs,suchasSAEsonMLPoutputs.
Futureworkontranscodersincludesdirectionssuchascomparingthefeatureslearnedbytranscoders
tothoselearnedbySAEs,seeingifthereareclassesoffeaturesthattranscodersstruggletolearn,
findinginterestingexamplesofnovelcircuits,andscalingcircuitanalysistolargermodels.
Overall,webelievethattranscodersareanexcitingnewdevelopmentforcircuitanalysisandhope
thattheycancontinuetoyielddeeperinsightsintomodelbehaviors.
Limitations Transcoders,likeSAEs,areapproximationstotheunderlyingmodel,andtheresulting
errormaylosekeyinformation. Wefindtranscoderstobeapproximatelyasunfaithfultothemodel’s
computationsasSAEsare(asmeasuredbythecross-entropyloss),althoughweleavecomparingthe
errorstofuturework. Ourcircuitanalysismethod(App. D.5)doesnotengagewithhowattention
patternsarecomputed,andtreatsthemasfixed. Apromisingdirectionoffutureworkwouldbetrying
toextendtranscoderstounderstandthecomputationofattentionpatterns,approximatingtheattention
softmax. Weonlypresentcircuitanalysisresultsforafewqualitativecasestudies,andourresults
wouldbestrongerwithmoresystematicanalysis.
10

Impactstatement
Thispaperseekstoadvancethefieldofmechanisticinterpretabilitybycontributinganewtoolfor
circuit analysis. We see this as foundational research, and expect the impact to come indirectly
fromfutureapplicationsofcircuitanalysissuchasunderstandinganddebuggingunexpectedmodel
behaviorandcontrollingandsteeringmodelstobemoreusefultousers.
AcknowledgmentsandDisclosureofFunding
Jacob and Philippe were funded by a grant from AI Safety Support Ltd. Jacob was additionally
fundedbyagrantfromtheLong-TermFutureFund. PhilippewasadditionallyfundedbyNSFGRFP
grantDGE-2036197. ComputewasgenerouslyprovidedbyYaleUniversity.
We would like to thank Andy Arditi, Lawrence Chan, and Matt Wearden for providing detailed
feedbackonourmanuscript. WewouldalsoliketothankSenthooranRajamanoharanandJuanDavid
Gilfordiscussionsduringtheresearchprocess,andJosephBloomforadviceonhowtouse(and
extend)theSAELenslibrary. Finally,wewouldliketothankJoshuaBatsonforadiscussionthat
inspiredustoinvestigatetranscodersinthefirstplace.
References
[1] Batson, J., Chen, B., and Jones, A. Using features for easy circuit identification,
2024. URLhttps://transformer-circuits.pub/2024/march-update/index.html#
feature-heads.
[2] Biderman,S.,Schoelkopf,H.,Anthony,Q.,Bradley,H.,O’Brien,K.,Hallahan,E.,Khan,M.A.,
Purohit,S.,Prashanth,U.S.,Raff,E.,Skowron,A.,Sutawika,L.,andvanderWal,O. Pythia:
ASuiteforAnalyzingLargeLanguageModelsAcrossTrainingandScaling,May2023. URL
http://arxiv.org/abs/2304.01373. arXiv:2304.01373[cs].
[3] Bills, S., Cammarata, N., Mossing, D., Tillman, H., Gao, L., Goh, G., Sutskever, I., Leike,
J., Wu, J., and Saunders, W. Language models can explain neurons in language mod-
els,2023.URLhttps://openaipublic.blob.core.windows.net/neuron-explainer/
paper/index.html.
[4] Bloom,J. OpenSourceSparseAutoencodersforallResidualStreamLayersofGPT2-Small,
2024. URLhttps://www.lesswrong.com/posts/f9EgfLSurAiqRJySD.
[5] Bloom,J. SAELensTraining,2024. URLhttps://jbloomaus.github.io/SAELens/.
[6] Bolukbasi,T.,Pearce,A.,Yuan,A.,Coenen,A.,Reif,E.,Viégas,F.,andWattenberg,M. An
interpretabilityillusionforbert. arXivpreprintarXiv:2104.07143,2021.
[7] Bricken,T.,Templeton,A.,Batson,J.,Chen,B.,Jermyn,A.,Conerly,T.,Turner,N.,Anil,C.,
Denison,C.,Askell,A.,Lasenby,R.,Wu,Y.,Kravec,S.,Schiefer,N.,Maxwell,T.,Joseph,N.,
Hatfield-Dodds,Z.,Tamkin,A.,Nguyen,K.,McLean,B.,Burke,J.E.,Hume,T.,Carter,S.,
Henighan,T.,andOlah,C. TowardsMonosemanticity: DecomposingLanguageModelsWith
DictionaryLearning. TransformerCircuitsThread,2023.
[8] Brown,T.B.,Mann,B.,Ryder,N.,Subbiah,M.,Kaplan,J.,Dhariwal,P.,Neelakantan,A.,
Shyam,P.,Sastry,G.,Askell,A.,Agarwal,S.,Herbert-Voss,A.,Krueger,G.,Henighan,T.,
Child, R., Ramesh, A., Ziegler, D. M., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E.,
Litwin,M.,Gray,S.,Chess,B.,Clark,J.,Berner,C.,McCandlish,S.,Radford,A.,Sutskever,I.,
andAmodei,D. LanguageModelsareFew-ShotLearners,July2020. URLhttp://arxiv.
org/abs/2005.14165. arXiv:2005.14165[cs].
[9] ChrisOlah. MechanisticInterpretability,Variables,andtheImportanceofInterpretableBases,
2022. URL https://transformer-circuits.pub/2022/mech-interp-essay/index.
html.
11

[10] Chrupała,G.andAlishahi,A. Correlatingneuralandsymbolicrepresentationsoflanguage. In
Proceedingsofthe57thAnnualMeetingoftheAssociationforComputationalLinguistics,pp.
2952–2962,2019. doi: 10.18653/v1/P19-1283. URLhttp://arxiv.org/abs/1905.06401.
arXiv:1905.06401[cs].
[11] Conmy,A.,Mavor-Parker,A.N.,Lynch,A.,Heimersheim,S.,andGarriga-Alonso,A. Towards
Automated Circuit Discovery for Mechanistic Interpretability, October 2023. URL http:
//arxiv.org/abs/2304.14997. arXiv:2304.14997[cs].
[12] Cunningham,H.,Ewart,A.,Riggs,L.,Huben,R.,andSharkey,L. SparseAutoencodersFind
HighlyInterpretableFeaturesinLanguageModels,October2023. URLhttp://arxiv.org/
abs/2309.08600. arXiv:2309.08600[cs].
[13] Dunefsky,J.andCohan,A. ObservablePropagation: AData-EfficientApproachtoUncover
Feature Vectors in Transformers, December 2023. URL http://arxiv.org/abs/2312.
16291. arXiv:2312.16291[cs].
[14] Dunefsky, J., Chlenski, P., Rajamanoharan, S., and Nanda, N. Case Studies in Reverse-
EngineeringSparseAutoencoderFeaturesbyUsingMLPLinearization,2024. URLhttps:
//www.alignmentforum.org/posts/93nKtsDL6YY5fRbQv. Published: AlignmentForum.
[15] Elhage, N., Nanda, N., Olsson, C., Henighan, T., Joseph, N., Mann, B., Askell, A., Bai, Y.,
Chen,A.,Conerly,T.,DasSarma,N.,Drain,D.,Ganguli,D.,Hatfield-Dodds,Z.,Hernandez,
D.,Jones,A.,Kernion,J.,Lovitt,L.,Ndousse,K.,Amodei,D.,Brown,T.,Clark,J.,Kaplan,J.,
McCandlish,S.,andOlah,C.AMathematicalFrameworkforTransformerCircuits.Transformer
CircuitsThread,2021.
[16] Elhage,N.,Hume,T.,Olsson,C.,Nanda,N.,Henighan,T.,Johnston,S.,ElShowk,S.,Joseph,
N., DasSarma, N., Mann, B., Hernandez, D., Askell, A., Ndousse, K., Jones, A., Drain, D.,
Chen,A.,Bai,Y.,Ganguli,D.,Lovitt,L.,Hatfield-Dodds,Z.,Kernion,J.,Conerly,T.,Kravec,
S., Fort, S., Kadavath, S., Jacobson, J., Tran-Johnson, E., Kaplan, J., Clark, J., Brown, T.,
McCandlish,S.,Amodei,D.,andOlah,C. Softmaxlinearunits. TransformerCircuitsThread,
2022. https://transformer-circuits.pub/2022/solu/index.html.
[17] Elhage, N., Hume, T., Olsson, C., Schiefer, N., Henighan, T., Kravec, S., Hatfield-Dodds,
Z., Lasenby, R., Drain, D., Chen, C., Grosse, R., McCandlish, S., Kaplan, J., Amodei, D.,
Wattenberg, M., and Olah, C. Toy Models of Superposition, September 2022. URL http:
//arxiv.org/abs/2209.10652. arXiv:2209.10652[cs].
[18] Ferrando,J.,Sarti,G.,Bisazza,A.,andCosta-jussà,M.R. APrimerontheInnerWorkings
ofTransformer-basedLanguageModels,May2024. URLhttp://arxiv.org/abs/2405.
00208. arXiv:2405.00208[cs]version: 2.
[19] Gandelsman, Y., Efros, A.A., andSteinhardt, J. InterpretingCLIP’sImageRepresentation
viaText-BasedDecomposition,March2024. URLhttp://arxiv.org/abs/2310.05916.
arXiv:2310.05916[cs].
[20] Geiger,A.,Lu,H.,Icard,T.,andPotts,C. CausalAbstractionsofNeuralNetworks,October
2021. URLhttp://arxiv.org/abs/2106.02997. arXiv:2106.02997[cs].
[21] Gokaslan,A.andCohen,V. OpenWebTextCorpus,2019.
[22] Goldowsky-Dill,N.,MacLeod,C.,Sato,L.,andArora,A. LocalizingModelBehaviorwith
PathPatching,May2023. URLhttp://arxiv.org/abs/2304.05969. arXiv:2304.05969
[cs].
[23] Gould, R., Ong, E., Ogden, G., and Conmy, A. Successor Heads: Recurring, Interpretable
AttentionHeadsInTheWild,December2023. URLhttp://arxiv.org/abs/2312.09230.
arXiv:2312.09230[cs].
[24] Gurnee,W.,Nanda,N.,Pauly,M.,Harvey,K.,Troitskii,D.,andBertsimas,D. FindingNeurons
inaHaystack: CaseStudieswithSparseProbing,June2023. URLhttp://arxiv.org/abs/
2305.01610. arXiv:2305.01610[cs].
12

[25] Hanna,M.,Liu,O.,andVariengien,A. HowdoesGPT-2computegreater-than?: Interpreting
mathematicalabilitiesinapre-trainedlanguagemodel,November2023. URLhttp://arxiv.
org/abs/2305.00586. arXiv:2305.00586[cs].
[26] Hanna,M.,Pezzelle,S.,andBelinkov,Y. HaveFaithinFaithfulness: GoingBeyondCircuit
OverlapWhenFindingModelMechanisms,2024. _eprint: 2403.17806.
[27] He, Z., Ge, X., Tang, Q., Sun, T., Cheng, Q., and Qiu, X. Dictionary Learning Improves
Patch-FreeCircuitDiscoveryinMechanisticInterpretability: ACaseStudyonOthello-GPT,
February2024. URLhttp://arxiv.org/abs/2402.12201. arXiv:2402.12201[cs].
[28] Heimersheim,S.andNanda,N. Howtouseandinterpretactivationpatching. arXivpreprint
arXiv:2404.15255,2024.
[29] Kissane, C., Krzyzanowski, R., Conmy, A., and Nanda, N. Attention SAEs Scale to GPT-
2 Small, 2024. URL https://www.alignmentforum.org/posts/FSTRedtjuHa4Gfdbr.
Published: AlignmentForum.
[30] Kramár,J.,Lieberum,T.,Shah,R.,andNanda,N. AtP*: Anefficientandscalablemethodfor
localizingLLMbehaviourtocomponents,2024. _eprint: 2403.00745.
[31] Li, M., Marks, S., and Mueller, A. dictionary_learning repository, 2023.
https://github.com/saprmarks/dictionary_learning?tab=readme-ov-file#extra-functionality-
supported-by-this-repo.
[32] Lieberum,T.,Rahtz,M.,Kramár,J.,Nanda,N.,Irving,G.,Shah,R.,andMikulik,V. DoesCir-
cuitAnalysisInterpretabilityScale? EvidencefromMultipleChoiceCapabilitiesinChinchilla,
July2023. URLhttp://arxiv.org/abs/2307.09458. arXiv:2307.09458[cs].
[33] Lipton,Z.C. Themythosofmodelinterpretability,2017.
[34] Marks,S.,Rager,C.,Michaud,E.J.,Belinkov,Y.,Bau,D.,andMueller,A. SparseFeature
Circuits: DiscoveringandEditingInterpretableCausalGraphsinLanguageModels,March
2024. URLhttp://arxiv.org/abs/2403.19647. arXiv:2403.19647[cs].
[35] McDougall, C., Conmy, A., Rushing, C., McGrath, T., and Nanda, N. Copy Suppression:
Comprehensively Understanding an Attention Head. ArXiv, abs/2310.04625, 2023. URL
https://api.semanticscholar.org/CorpusID:263831290.
[36] Nanda,N. Opensourcereplication&commentaryonanthropic’sdictionarylearningpaper.
AlignmentForum,2023. https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk.
[37] Nanda, N. and Bloom, J. TransformerLens, 2022. URL https://github.com/
TransformerLensOrg/TransformerLens.
[38] Nanda, N., Rajamanoharan, S., Kram\’ar, J., and Shah, R. Fact Finding: Attempting to
Reverse-EngineerFactualRecallontheNeuronLevel,December2023. URLhttps://www.
alignmentforum.org/posts/iGuwZTHWb6DFY3sKB. PublicationTitle: AlignmentForum.
[39] NeelNanda. AttributionPatching: ActivationPatchingAtIndustrialScale,2024. URLhttps:
//www.neelnanda.io/mechanistic-interpretability/attribution-patching.
[40] Olah,C.,Mordvintsev,A.,andSchubert,L. Featurevisualization. Distill,2017. doi: 10.23915/
distill.00007. https://distill.pub/2017/feature-visualization.
[41] Olah, C., Cammarata, N., Schubert, L., Goh, G., Petrov, M., and Carter, S. Zoom In: An
Introduction to Circuits. Distill, 5(3):e00024.001, March 2020. ISSN 2476-0757. doi: 10.
23915/distill.00024.001. URLhttps://distill.pub/2020/circuits/zoom-in.
[42] Olsson,C.,Elhage,N.,Nanda,N.,Joseph,N.,DasSarma,N.,Henighan,T.,Mann,B.,Askell,
A.,Bai,Y.,Chen,A.,Conerly,T.,Drain,D.,Ganguli,D.,Hatfield-Dodds,Z.,Hernandez,D.,
Johnston,S.,Jones,A.,Kernion,J.,Lovitt,L.,Ndousse,K.,Amodei,D.,Brown,T.,Clark,J.,
Kaplan,J.,McCandlish,S.,andOlah,C. In-contextLearningandInductionHeads,September
2022. URLhttp://arxiv.org/abs/2209.11895. arXiv:2209.11895[cs].
13

[43] OpenAI,Achiam,J.,Adler,S.,Agarwal,S.,Ahmad,L.,Akkaya,I.,Aleman,F.L.,Almeida,
D.,Altenschmidt,J.,Altman,S.,Anadkat,S.,Avila,R.,Babuschkin,I.,Balaji,S.,Balcom,V.,
Baltescu,P.,Bao,H.,Bavarian,M.,Belgum,J.,Bello,I.,Berdine,J.,Bernadett-Shapiro,G.,
Berner,C.,Bogdonoff,L.,Boiko,O.,Boyd,M.,Brakman,A.-L.,Brockman,G.,Brooks,T.,
Brundage,M.,Button,K.,Cai,T.,Campbell,R.,Cann,A.,Carey,B.,Carlson,C.,Carmichael,
R.,Chan,B.,Chang,C.,Chantzis,F.,Chen,D.,Chen,S.,Chen,R.,Chen,J.,Chen,M.,Chess,
B.,Cho,C.,Chu,C.,Chung,H.W.,Cummings,D.,Currier,J.,Dai,Y.,Decareaux,C.,Degry,
T.,Deutsch,N.,Deville,D.,Dhar,A.,Dohan,D.,Dowling,S.,Dunning,S.,Ecoffet,A.,Eleti,
A., Eloundou, T., Farhi, D., Fedus, L., Felix, N., Fishman, S. P., Forte, J., Fulford, I., Gao,
L.,Georges,E.,Gibson,C.,Goel,V.,Gogineni,T.,Goh,G.,Gontijo-Lopes,R.,Gordon,J.,
Grafstein,M.,Gray,S.,Greene,R.,Gross,J.,Gu,S.S.,Guo,Y.,Hallacy,C.,Han,J.,Harris,J.,
He,Y.,Heaton,M.,Heidecke,J.,Hesse,C.,Hickey,A.,Hickey,W.,Hoeschele,P.,Houghton,
B.,Hsu,K.,Hu,S.,Hu,X.,Huizinga,J.,Jain,S.,Jain,S.,Jang,J.,Jiang,A.,Jiang,R.,Jin,
H.,Jin,D.,Jomoto,S.,Jonn,B.,Jun,H.,Kaftan,T.,Kaiser,L.,Kamali,A.,Kanitscheider,I.,
Keskar,N.S.,Khan,T.,Kilpatrick,L.,Kim,J.W.,Kim,C.,Kim,Y.,Kirchner,J.H.,Kiros,
J., Knight, M., Kokotajlo, D., Kondraciuk, L., Kondrich, A., Konstantinidis, A., Kosic, K.,
Krueger, G., Kuo, V., Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D., Li, C.M.,
Lim,R.,Lin,M.,Lin,S.,Litwin,M.,Lopez,T.,Lowe,R.,Lue,P.,Makanju,A.,Malfacini,
K.,Manning,S.,Markov,T.,Markovski,Y.,Martin,B.,Mayer,K.,Mayne,A.,McGrew,B.,
McKinney,S.M.,McLeavey,C.,McMillan,P.,McNeil,J.,Medina,D.,Mehta,A.,Menick,J.,
Metz,L.,Mishchenko,A.,Mishkin,P.,Monaco,V.,Morikawa,E.,Mossing,D.,Mu,T.,Murati,
M.,Murk,O.,Mély,D.,Nair,A.,Nakano,R.,Nayak,R.,Neelakantan,A.,Ngo,R.,Noh,H.,
Ouyang,L.,O’Keefe,C.,Pachocki,J.,Paino,A.,Palermo,J.,Pantuliano,A.,Parascandolo,G.,
Parish,J.,Parparita,E.,Passos,A.,Pavlov,M.,Peng,A.,Perelman,A.,Peres,F.d.A.B.,Petrov,
M.,Pinto,H.P.d.O.,Michael,Pokorny,Pokrass,M.,Pong,V.H.,Powell,T.,Power,A.,Power,
B.,Proehl,E.,Puri,R.,Radford,A.,Rae,J.,Ramesh,A.,Raymond,C.,Real,F.,Rimbach,
K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S.,
Sastry,G.,Schmidt,H.,Schnurr,D.,Schulman,J.,Selsam,D.,Sheppard,K.,Sherbakov,T.,
Shieh,J.,Shoker,S.,Shyam,P.,Sidor,S.,Sigler,E.,Simens,M.,Sitkin,J.,Slama,K.,Sohl,
I.,Sokolowsky,B.,Song,Y.,Staudacher,N.,Such,F.P.,Summers,N.,Sutskever,I.,Tang,J.,
Tezak, N., Thompson, M.B., Tillet, P., Tootoonchian, A., Tseng, E., Tuggle, P., Turley, N.,
Tworek,J.,Uribe,J.F.C.,Vallone,A.,Vijayvergiya,A.,Voss,C.,Wainwright,C.,Wang,J.J.,
Wang,A.,Wang,B.,Ward,J.,Wei,J.,Weinmann,C.J.,Welihinda,A.,Welinder,P.,Weng,J.,
Weng,L.,Wiethoff,M.,Willner,D.,Winter,C.,Wolrich,S.,Wong,H.,Workman,L.,Wu,S.,
Wu,J.,Wu,M.,Xiao,K.,Xu,T.,Yoo,S.,Yu,K.,Yuan,Q.,Zaremba,W.,Zellers,R.,Zhang,C.,
Zhang,M.,Zhao,S.,Zheng,T.,Zhuang,J.,Zhuk,W.,andZoph,B. GPT-4TechnicalReport,
March2024. URLhttp://arxiv.org/abs/2303.08774. arXiv:2303.08774[cs].
[44] Radford,A.,Wu,J.,Child,R.,Luan,D.,Amodei,D.,andSutskever,I. LanguageModelsare
UnsupervisedMultitaskLearners. Technicalreport,OpenAI,2019.
[45] Rajamanoharan,S.,Conmy,A.,Smith,L.,Lieberum,T.,Varma,V.,Kramár,J.,Shah,R.,and
Nanda,N. ImprovingDictionaryLearningwithGatedSparseAutoencoders,April2024. URL
http://arxiv.org/abs/2404.16014. arXiv:2404.16014[cs].
[46] Team,G.,Anil,R.,Borgeaud,S.,Wu,Y.,Alayrac,J.-B.,Yu,J.,Soricut,R.,Schalkwyk,J.,Dai,
A.M.,Hauth,A.,etal. Gemini: afamilyofhighlycapablemultimodalmodels. arXivpreprint
arXiv:2312.11805,2023.
[47] Templeton,A.,Batson,J.,Jermyn,A.,andOlah,C. PredictingFutureActivations,January
2024. URL https://transformer-circuits.pub/2024/jan-update/index.html#
predict-future.
[48] Templeton,A.,Conerly,T.,Marcus,J.,Lindsey,J.,Bricken,T.,Chen,B.,Pearce,A.,Citro,
C.,Ameisen,E.,Jones,A.,Cunningham,H.,Turner,N.L.,McDougall,C.,MacDiarmid,M.,
Freeman, C. D., Sumers, T. R., Rees, E., Batson, J., Jermyn, A., Carter, S., Olah, C., and
Henighan,T. Scalingmonosemanticity: Extractinginterpretablefeaturesfromclaude3sonnet.
Transformer Circuits Thread, 2024. URL https://transformer-circuits.pub/2024/
scaling-monosemanticity/index.html.
14

[49] Vig, J., Gehrmann, S., Belinkov, Y., Qian, S., Nevo, D., Singer, Y., and Shieber, S.
Investigating Gender Bias in Language Models Using Causal Mediation Analysis. In
Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M. F., and Lin, H. (eds.), Advances in
Neural Information Processing Systems, volume 33, pp. 12388–12401. Curran Associates,
Inc.,2020. URLhttps://proceedings.neurips.cc/paper_files/paper/2020/file/
92650b2e92217715fe312e6fa7b90d82-Paper.pdf.
[50] Wang, K., Variengien, A., Conmy, A., Shlegeris, B., and Steinhardt, J. Interpretability in
theWild: aCircuitforIndirectObjectIdentificationinGPT-2small,November2022. URL
http://arxiv.org/abs/2211.00593. arXiv:2211.00593[cs].
[51] Yun,Z.,Chen,Y.,Olshausen,B.A.,andLeCun,Y. Transformervisualizationviadictionary
learning: contextualizedembeddingasalinearsuperpositionoftransformerfactors,2023.
[52] Zhang, F.andNanda, N. TowardsBestPracticesofActivationPatchinginLanguageMod-
els: Metrics and Methods, January 2024. URL http://arxiv.org/abs/2309.16042.
arXiv:2309.16042[cs].
15

A Assetsused
Table2: Assetsusedinpreparingthispaper,alongwithlicensesandlinks
Assettype Assetname Link License Citation
Code TransformerLens GitHub: TransformerLens MIT [37]
Code SAELens Github: SAELens MIT [5]
Data OpenWebText HuggingFace: OpenWebText CC0-1.0 [21]
Model GPT2-small HuggingFace: GPT2 MIT [44]
Model Pythia-410M HuggingFace: Pythia-410M Apache-2.0 [2]
Model Pythia-1.4B HuggingFace: Pythia-1.4B Apache-2.0 [2]
B Computedetails
The most compute-intensive parts of the research presented in this work were training the SAEs
andtranscodersusedinSection4.2,alongwiththesetofGPT2-smalltranscodersusedinSections
5.1and5.2. TrainingalloftheseSAEsandtranscodersinvolvedGPUs. TheSAEsandtranscoders
fromSection4.2weretrainedonaninternalclusterusinganA100GPUwith80GBofVRAM.The
VRAMusedbyeachtrainingrunrangedfromapproximately16GBfortheGPT2-smallrunsto
approximately60GBforthePythia-1.4Bruns. Thetimetakenbyeachtrainingrunrangedfrom
approximately30minutesfortheGPT2-smalltranscoders/SAEstoapproximately3.5hoursforthe
Pythia-1.4Bruns.
ThetranscodersthatweretrainedoneachlayerofGPT2-smallweretrainedusingacloudprovider,
withasimilaramountoftimeandVRAMusedpertrainingrun. Forthesetranscoders,ahyperpa-
rametersweepwasperformedthatinvolvedapproximately200trainingruns,whichdidnotproduce
resultsusedinthefinalpaper.
Nosignificantamountofstoragewasused,asdatasetswerestreamedduringtraining.
Inadditiontothesetrainingruns,ourcasestudieswerecarriedoutoninternalclusternodeswith
GPUs. Thesecasestudiesusednomorethan6GBofVRAM.Thetotalamountofcomputeused
duringeachcasestudyisvariable(dependingonhowin-depthonewantstoinvestigateacasestudy),
but is de minimis in comparison to the training runs. The same goes for the computation of top
activatingexamplesusedinSection4.1.
C SAEdetails
Sparseautoencoders(SAEs)areautoencoderstrainedtodecomposeamodel’sactivationsatagiven
pointintoasparselinearcombinationoffeaturevectors. Asahypotheticalexample,giventheinput
“Sallythrewtheballtome”,anSAEmightdecomposethemodel’sactivationsonthetoken meintoa
linearcombinationofa“personalpronoun”featurevector,an“indirectobject”feature,anda“playing
sports”feature—whereallofthesefeaturevectorsareautomaticallylearnedbytheSAE.AnSAE’s
architecturecanbeexpressedas
z (x)=ReLU(W x+b ) (9)
SAE enc enc
SAE(x)=W z (x)+b , (10)
dec SAE dec
where W
enc
∈ Rdfeatures×dmodel, W
dec
∈ Rdmodel×dfeatures, b
enc
∈ Rdfeatures, b
dec
∈ Rdmodel, d
features
is
thenumberoffeaturevectorsintheSAE,andd isthedimensionalityofthemodelactivations.
model
Usually,d isfargreaterthand .
features model
Intuitively, Equation 9 transforms the neuron activations x into a sparse vector of SAE feature
activationsz (x). EachfeatureinanSAEisassociatedwithan“encoder”vector(thei-throwof
SAE
W )anda“decoder”vector(thei-thcolumnofW ). Equation10thenreconstructstheoriginal
enc dec
activationsasalinearcombinationofdecodervectors,weightedbythefeatureactivations.
ThebasiclossfunctiononwhichSAEsaretrainedis
L (x)=∥x−SAE(x)∥2+λ ∥z (x)∥ , (11)
SAE 2 1 SAE 1
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
reconstructionloss sparsitypenalty
16

where λ is a hyperparameter and ∥·∥ denotes the L norm. The first term in the loss is the
1 1 1
reconstruction loss associated with the SAE. The second term in the loss is a sparsity penalty,
whichapproximatelymeasuresthenumberoffeaturesactiveoneachinput(theL normisusedasa
1
differentiableapproximationoftheL “norm”).SAEsarethuspushedtoreconstructinputsaccurately
0
withasparsenumberoffeatures,withλ controllingtheaccuracy-sparsitytradeoff. Empirically,the
1
resultofthisisthatSAEslearntodecomposemodelactivationsintohighlyinterpretablefeatures[7].
AstandardmethodforquantitativelyevaluatinganSAE’sperformanceisasfollows. Tomeasure
its sparsity, evaluate the mean number of features active on any given input (the mean L ). To
0
measureitsaccuracy,replacetheoriginallanguagemodel’sactivationswiththeSAE’sreconstructed
activations and measure the change in the language model’s loss (in this paper, this is the cross
entropylossfornexttokenprediction).
D Detaileddescriptionofcircuitanalysis
D.1 Notation
x(l,t)denotesthehiddenstatefortokentatlayerlbeforetheattentionsublayer.
pre
x(l,t) denotesthehiddenstatefortokentatlayerlbeforetheMLPsublayer.
mid
Whenwewanttorefertothehiddenstateofthemodelforalltokens,wewilldobyomittingthe
tokenindex,writingx(
p
l
r
,1
e
:t)andx(
m
l,
i
1
d
:t). ThesearematricesofsizeRdmodel×ntokens,whered
model
isthe
dimensionalityofmodelactivationvectorsandn isthenumberofinputtokens.
tokens
TheMLPsublayeratlayerlisdenotedbyMLP(l)(·). Similarly,thetranscoderforthelayerlMLP
isdenotedbyTC(l)(·).
Asforattentionsublayers: followingElhageetal.[15],eachattentionsublayercanbedecomposed
into the sum of n independently-acting attention heads. Each attention head depends on the
heads
hiddenstatesofalltokensintheinput,butalsodistinguishesthetokenwhosehiddenstateistobe
modifiedbytheattentionhead. Thus,theoutputofthelayerlattentionsublayerfortokentisdenoted
(cid:16) (cid:17)
(cid:80) attn(l,h) x(l,t);x(l,1:t) .
headh pre pre
Eachattentionheadcanfurtherbedecomposedasasumover“source”tokens. Inparticular,the
outputoflayerlattentionheadhfortokentcanbewrittenas
attn(l,h) (cid:16) x(l,t);x(l,1:t) (cid:17) = (cid:88) score(l,h) (cid:16) x(l,t),x(l,s) (cid:17) W(l,h)x(l,s) (12)
pre pre pre pre OV pre
sourcetokens
Here,score(l,h) :Rdmodel×dmodel →Risascalar“scoring”functionthatweightstheimportanceofeach
sourcetokentothedestinationtoken. Additionally,W(l,h) isalow-rankRdmodel×dmodel matrixthat
OV
transformsthehiddenstateofeachsourcetoken. score(l,h)isoftenreferredtoasthe“QKcircuit”of
attentionandW(l,h)isoftenreferredtoasthe“OVcircuit”ofattention.
OV
D.2 DerivationofEquation7
Wewanttounderstandwhatcausesfeaturei′inthetranscoderatlayerl′toactivateontokent. The
activationofthisfeatureisgivenby
ReLU
(cid:16) f(l′,i′)·x(l′,t)+b(l′,i′) (cid:17)
, (13)
enc mid enc
wheref(l′,i′) isthei′-throwofW forthelayerl′ transcoderandb(l′,i′) isthelearnedencoder
enc enc enc
biasforfeaturei′inthelayerl′transcoder. Therefore,ifweignoretheconstantbiastermb(l′,i′),then,
enc
assumingthatthisfeatureisactive(whichallowsustoignoretheReLU),theactivationoffeaturei′
dependssolelyonf(l′,i′)·x(l′,t). Becauseofresidualconnectionsinthetransformer,x(l′,t)canbe
enc mid mid
decomposedasthesumoftheoutputsofallpreviouscomponentsinthemodel. Forinstance,ina
17

two-layermodel,ifx(2,t)isthehiddenstateofthemodelrightbeforethesecondMLPsublayer,then
mid
x(2,t) = (cid:88) attn(2,h) (cid:16) x(2,t);x(2,1:t) (cid:17) +MLP(1) (cid:16) x(1,t) (cid:17) + (cid:88) attn(1,h) (cid:16) x(1,t);x(1,1:t) (cid:17) .
mid pre pre mid pre pre
h h
(14)
Becauseoflinearity,thismeansthattheamountthatMLP(1) (cid:16) x(1,t) (cid:17) contributestof(2,i′)·x(2,t)is
mid enc mid
givenby
(cid:16) (cid:17)
f(2,i′)·MLP(1) x(1,t) . (15)
enc mid
ThisisgenerallytrueforunderstandingthecontributionofMLPltotheactivationoffeaturei′ in
transcoderl′,wheneverl<l′.
Now, if the layer l transcoder is a sufficiently good approximation to the layer l MLP, we can
replacethelatterwiththeformer: f(l′,i′)·MLP(l) (cid:16) x(l,t) (cid:17) ≈f(l′,i′)·TC(l) (cid:16) x(l,t) (cid:17) . Wecanfurther
enc mid enc mid
(cid:16) (cid:17)
decompose this into individual transcoder features: TC(l) x(l,t) = (cid:80) z(l,j)(x(l,t))f(l,j).
mid featurej TC mid dec
Thus,againtakingadvantageoflinearity,wehave
f(l′,i′)·MLP(l) (cid:16) x(l,t) (cid:17) ≈f(l′,i′)· (cid:88) z(l,j)(x(l,t))f(l,j) (16)
enc mid enc TC mid dec
featurej
= (cid:88) z(l,j)(x(l,t)) (cid:16) f(l′,i′)·f(l,j) (cid:17) (17)
TC mid enc dec
featurej
Therefore,theattributionoffeatureiintranscoderlontokentisgivenby
(cid:16) (cid:17)
z(l,j)(x(l,t)) f(l′,i′)·f(l,j) . (18)
TC mid enc dec
D.3 Attributionthroughattentionheads
Sofar,wehaveaddressedhowtofindtheattributionofalower-layertranscoderfeaturedirectlyon
ahigher-layertranscoderfeatureatthesametoken. Buttranscoderfeaturescanalsobemediated
byattentionheads. Wewillthusextendtheaboveanalysistoaccountforfindingtheattributionof
transcoderfeaturesthroughtheOVcircuitofanattentionhead.
As before, we want to understand what causes feature i′ in the layer l′ transcoder to activate on
tokent. Givenattentionheadhatlayerlwithl <l′,thesameargumentsasbeforeimplythatthe
contributionofthisattentionheadtofeaturei′ isgivenbyf(l′,i′)·attn(l,h) (cid:16) x(l,t);x(l,1:t) (cid:17) . This
enc pre pre
canfurtherbedecomposedas
(cid:32) (cid:33)
f(l′,i′)· (cid:88) score(l,h) (cid:16) x(l,t),x(l,s) (cid:17) W(l,h)x(l,s) (19)
enc pre pre OV pre
sourcetokens
= (cid:88) score(l,h) (cid:16) x(l,t),x(l,s) (cid:17)(cid:18)(cid:16) f(l′,i′) (cid:17)T W(l,h)x(l,s) (cid:19) (20)
pre pre enc OV pre
sourcetokens
= (cid:88) score(l,h) (cid:16) x(l,t),x(l,s) (cid:17)(cid:18)(cid:18)(cid:16) W(l,h) (cid:17)T f(l′,i′) (cid:19) ·x(l,s) (cid:19) . (21)
pre pre OV enc pre
sourcetokens
Fromthis,wenowhavethatthecontributionoftokensatlayerlthroughheadhisgivenby
(cid:16) (cid:17)(cid:18)(cid:18)(cid:16) (cid:17)T (cid:19) (cid:19)
score(l,h) x(l,t),x(l,s) W(l,h) f(l′,i′) ·x(l,s) . (22)
pre pre OV enc pre
Thenextstepistonotethatx(l,s)can,inturn,bedecomposedintotheoutputofMLPsublayers(or
pre
alternatively,transcoderfeatures),theoutputofattentionheads,andtheoriginaltokenembedding.
These previous-layer components affect the contribution to the original feature through both the
QKcircuitofattentionandtheOVcircuit. Thismeansthattheseprevious-layercomponentscan
haveverynonlineareffectsonthecontribution. Weaddressthisbyfollowingthestandardpractice
18

(cid:16) (cid:17)
introduced by Elhage et al. [15], which is to treat the QK circuit scores score(l,h) x(l,t),x(l,s)
pre pre
as fixed, and only look at the contributions through the OV circuit. While this does prevent us
fromunderstandingtheextenttowhichtranscoderfeaturescontributetophenomenasuchasQK
composition,nevertheless,theOVcircuitaloneisextremelyinformative. Afterall,iftheQKcircuit
determineswhichtokensinformationistakenfrom,thentheOVcircuitdetermineswhatinformation
istakenfromeachtoken—andthiscanproveimmenselyvaluableincircuitanalysis.
Thus, let us continue by treating the QK scores as fixed. Referring back to Equation 22, if y is
theoutputofsomepreviouslayercomponent, whichexistsintheresidualstreamx(l,s), thenthe
pre
contributionofytotheoriginaltranscoderfeaturei′throughtheOVcircuitoflayerlattentionhead
hisgivenbyy·p′,where
(cid:16) (cid:17)
p′ =score(l,h) x(l,t),x(l,s) p, and (23)
pre pre
(cid:16) (cid:17)T
p= W(l,h) f(l′,i′). (24)
OV enc
Onewaytolookatthisisthatp′ isafeaturevector. Justlikewithtranscoderfeatures,theextent
towhichthefeaturevectorp′isactivatedbyagivenvectoryisgivenbythedotproductofyand
p′. Treatingp′asafeaturevectorlikethismeansthatwecanextendallofthetechniquespresented
inSection3.2toanalyzep′. Forexample,wecantakethede-embeddingofp′todeterminewhich
tokensinthemodel’svocabularywhenmediatedbytheOVcircuitoflayerlattentionheadhcause
layerl′transcoderfeaturei′toactivatethemost. Wecanalsoreplacethef(l′,i′)terminEquation7
enc
withp′inordertoobtaininput-invariantandinput-dependentinformationaboutwhichtranscoder
featureswhenmediatedbythisOVcircuitmakethegreatestcontributiontotheactivationoflayer
l′ transcoderfeaturei′. Inthismanner, wehaveextendedourattributiontechniquestodealwith
attention.
D.4 Recursingonasinglecomputationalpath
At this point, we understand how to obtain the attribution from an earlier-layer transcoder fea-
ture/attention head to a later-layer feature vector. The next step is to understand in turn what
contributestotheseearlier-layerfeaturesorheads. Doingsowillallowustoiterativelycompute
attributionsalonganentirecomputationalgraph.
Todothis,wewillextendtheintuitionpresentedinEquation23andpreviouslydiscussedbyDunefsky
&Cohan[13],whichistopropagateourfeaturevectorbackwardsthroughthecomputationalpath.4
Startingattheendofthecomputationalpath,foreachnodeinthecomputationalpath,wecompute
theattributionofthenodetowardscausingthecurrentfeaturevectortoactivate;wethencomputea
newfeaturevector,andrepeattheprocessusingtheprecedingnodeandthisnewfeaturevector.
Inparticular,ateverynode,wewanttocomputethenewfeaturevectorf suchthatitsatisfiesthe
followingproperty. Letc′beanode(e.g. atranscoderfeatureoranattentionhead),x′bethevector
ofinputactivationstothenodec′(i.e. theresidualstreamactivationsbeforethenodec′),y′bethe
outputofc′,a′betheattributionofc′tosomelater-layerfeature,andf′bethecurrentfeaturevector
to which we are computing the attribution of c′. Noting that a′ = f′ ·y′, then we want our new
featurevectorf tosatisfy
f ·x′ =a′. (25)
Thisisbecauseiff satisfiesthisproperty,thenwecantakeadvantageofthelinearityoftheresidual
streamtoeasilycalculatetheattributionfromanearlier-layercomponentctothecurrentnodec′. In
particular,iftheoutputofcisthevectory,thenthisattributionisjustgivenbyf·y.Anotherimportant
consequenceofEquation25andthelinearityoftheresidualstreamisthatthetotalattributiona′of
nodec′isgivenby
(cid:88)
a′ = f ·y (26)
y
wherewesumoveralltheoutputsyofallearliernodesinthemodel’scomputationalgraph(including
transcoderfeaturesandattentionheads,butalsotokenembeddingsandlearnedconstantbiasvectors,
whichareleafnodesinthecomputationalgraph).
4The similarity to backpropagation is not coincidental, as it can be shown that the method about to be
describedcomputesthe“input-times-gradient”attributionoftenusedintheexplanabilityliterature.
19

Ifc′isattentionheadhinlayerlandweareconsideringthecontributionfromtheinputactivations
x(l,s)atsourcetokenpositions,thenEquation22tellsusthat
pre
(cid:16) (cid:17)(cid:18)(cid:16) (cid:17)T (cid:19)
f =score(l,h) x(l,t),x(l,s) W(l,h) f′ (27)
pre pre OV
wheretokenpositiontisthetokenpositioncorrespondingtothelater-layerfeaturef′. Andifc′is
transcoderfeatureiatlayerl,thenEquation18impliesthat
(cid:16) (cid:17)
f = f′·f(l,i) f(l,i). (28)
dec enc
Thereisonecaveat,however,thatmustbenoted. Beforeeverysublayerinthetransformerarchitec-
turesconsideredinthispaper(thatis,beforeeveryMLPsublayerandattentionsublayer),thereisa
LayerNormnonlinearity. NeelNanda[39]providesintuitionthatLayerNormnonlinearitiescanbe
approximatedasalineartransformationthatscalesitsinputbyaconstant;Dunefsky&Cohan[13]
providefurthertheoreticalmotivationandempiricalresultssuggestingthatthisisreasonable. We
followthisapproachinourcircuitanalysisbymultiplyingeachf featurevectorbytheappropriate
LayerNorm“scalingconstant”(whichisempiricallyestimatedbytakingtheratioofthenormofthe
pre-LayerNormactivationvectortothepost-LayerNormactivationvector).
D.5 Fullcircuit-findingalgorithm
Atthispoint,wearereadytopresentthefullversionofourcircuit-findingalgorithm. Thegreedy
computational-path-findingalgorithmispresentedasAlgorithm1. Thisalgorithmincorporatesthe
ideaspresentedinApp. D.4inordertoevaluatetheattributionofnodesincomputationalpaths;given
asetofcomputationalpathsoflengthL,itobtainsasetofimportantcomputationalpathsoflength
L+1bycomputingallpossibleextensionstothecurrentlength-Lpaths,andthenkeepingonlythe
N pathswiththehighestattributions. Notethatforthepurposeofclarity,thedescriptionpresented
hereislessefficientthanouractualimplementation;italsodoesnotincludetheLayerNormscaling
constantsdiscussedabove.
Next,givenasetofcomputationalpaths,Algorithm2convertsthissetintoasinglecomputational
graph. The main idea is to combine all of the paths into a single graph such that the attribution
of a node in the graph is the sum of its attributions in all distinct computational paths beginning
atthatnode. Similarly, theattributionofanedgeinthegraphisthesumofitsattributionsinall
distinctcomputationalpathsbeginningwiththatedge. Thispreventsdouble-countingofattributions.
Assumingzerotranscodererror,Equation26impliesthatinagraphproducedbyAlgorithm2from
thefullsetofcomputationalpathsinthemodel(includingbiasterms),theattributionofeachnodeis
thesumoftheattributionsofalloftheincomingedgestothatnode. Toaccountfortranscodererror,
andtoaccountforthefactthatnotallcomputationalpathsareincludedinthegraph,errornodescan
beaddedtothegraph,followingtheapproachofMarksetal.[34].
E DetailsonSection4.2SAE/transcodertraining
Inthissection,weprovidedetailsonthehyperparametersusedtotraintheSAEsandtranscoders
evaluatedinSection4.2.
AllSAEsandtranscodersweretrainedwithalearningrateof2·10−5 usingtheAdamoptimizer.
Hyperparameters(learningrateandλ sparsitycoefficient)werechosenlargelybasedontrial-and-
1
error.
ThelossfunctionsusedwerethevanillaSAEandtranscoderlossfunctionsasspecifiedinSection3.1
andAppendixC.Noneuronresamplingmethodswereusedduringtraining.
SAEsweretrainedonoutputactivationsoftheMLPlayer. Transcodersweretrainedonthepost-
LayerNorminputactivationstotheMLPlayerandtheoutputactivationsoftheMLPlayer. Wechose
totrainSAEsontheoutputactivationsbecausewhenmeasuringcross-entropylosswithtranscoders,
theoutputactivationsoftheMLParereplacedwiththetranscoderoutput;itisthusmostvalidto
comparetranscoderstoSAEsthatreplacetheMLPoutputactivationsaswell.
ThenumberoffeaturesintheSAEsandtranscoderswasalways32×thedimensionalityofthemodel
onwhichtheyweretrained. ForGPT2-small,themodeldimensionalityis768. ForPythia-410M,the
modeldimensionalityis1024. ForPythia-1.4B,themodeldimensionalityis2048.
20

Algorithm1Greedycomputational-path-finding
Input:
f′ Afeaturevector
l′ Thelayerfromwhichf′came.
t Thetokenpositionassociatedwithfeaturef′.
a Theactivationoff′
L Thenumberofiterationstopathfindfor
N Thenumberofpathstoretainaftereachiteration
Theinputpromptonwhichwewillperformcircuitanalysis
Output:
Asetofcomputationalpathsimportantforcausingf′toactivate
Initialize P ← {[(f′,l′,t′,a′)]} {P will be our working set of computational paths. Each
computationalpathisalistoffeaturevectorspairedwiththeirattributions. }
InitializeP ←{}{Thiswillcontainouroutput}
out
Runthemodelontheinputprompt,cachingallofitsactivations.
whileL>0do
InitializeP ←{}{Thiswillcontainthenextiterationofcomputationalpaths}
next
foreachP ∈P do
Setf ,l ,t ,a tothevaluesinthelastelementofP
cur cur cur cur
InitializeA←{}{Thesetofattributionsofalllower-layerfeatures}
foreachtranscoderfeatureiinlayerlwherel<l do
cur
Insert (cid:16)(cid:16) f ·f(l,i) (cid:17) f(l,i),l,t,z (x(l,t′)) (cid:16) f ·f(l,i) (cid:17)(cid:17) intoA
cur dec enc TC mid cur dec
endfor
foreachattentionheadhinlayerlattokentwherel<l andt≤t do
cur cur
(cid:16) (cid:17)
ComputetheattentionscoreS ←score(l,h) x(lcur,tcur),x(l,t)
pre pre
(cid:18)(cid:16) (cid:17)T (cid:19)
Computethefeaturevectorf ←S W(l,h) f
new OV cur
Computetheattributiona ←f ·x(l,t)
new new pre
Insert(f ,l,t,a )intoA
new new
endfor
Computetheembeddingattributiona embed ←f cur ·x0 p , r t e cur
Insert(0,0,t ,a )intoA
cur embed
foreach(f ,l ,t ,a )∈Ado
new new new new
ifa isamongthetopN valuesofa containedinAthen
new new
Append(f ,l ,t ,a )topathP andinsertintoP
new new new new next
endif
endfor
endfor
RemoveallpathsinP exceptforthepathswheretheattributionoftheearliest-layerfeature
next
vectorinthepathisamongthetopN inP
next
AppendallpathsinP toP
next out
P ←P
next
L←L−1
endwhile
returnP
out
TheSAEsandtranscodersweretrainedon60milliontokensoftheOpenWebTextdataset. Thebatch
sizewas4096examplesperbatch. Eachexamplecontainsacontextwindowof128tokens;when
evaluatingtheSAEsandtranscoders,wedidsoonexamplesoflength128tokensaswell.
Thesamerandomseed(42)wasusedtoinitializeallSAEsandtranscodersduringthetrainingprocess.
Inparticular,thismeantthattrainingdatawasreceivedinthesameorderbyallSAEsandtranscoders.
21

Algorithm2Paths-to-graph
Input:
P Asetofcomputationalpaths
Output: G =(V,E)AcomputationalgraphformedfromthepathsofP.
InitializeS ←{}{Asetofalready-seencomputationalpathprefixes,topreventusfromdouble-
countingattributions}
InitializeV ←{}{Adictionarymappingnodestotheirattributions}
InitializeE ←{}{Adictionarymappingedges(nodepairs)totheirattributions}
forEachP inP do
fori∈[1...|P|]do
s←theprefixofP uptoandincludingthei-thelement
ifs∈S then
Skipthisiterationoftheloop.
endif
InsertsintoS.
ifshaslength1then
Letnbetheonlynodeins.
SetV[n]totheattributionofn.
else
Setn ←P[i−1],n ←P[i]{Earlier-layernodescomelaterinthecomputational
parent child
pathsreturnedbyAlgorithm1}
Addtheattributionofn toV[n ]
child child
Addtheattributionofn toE[(n ,n )]
child child parent
endif
endfor
endfor
returnV,E
F DetailsonSection4.1
The transcoder used in the interpretability comparison was the Pythia-410M layer 15 transcoder
trainedwithλ sparsitycoefficient5.5×10−5fromSection4.2. TheSAEusedinthecomparison
1
wasaPythia-410Mlayer15SAEtrainedonMLPinputswithλ =7.0×10−5. WeusedanSAE
1
trainedonMLPinputsratherthanonetrainedonMLPoutputs(asin§4.2)becausetheinterpretability
comparisoninvolveslookingatwhichexamplescausefeaturestoactivate. This,inturn,iswholly
determinedbytheencoderfeaturevectors. Becausethetranscoder’sencoderfeaturevectorslive
intheMLPinputspace,itisthusmostvalidtocomparethetranscodertoanSAEwhoseencoder
featurevectorsalsoliveintheMLPinputspace.
Thistranscoder-SAEpairwaschosenbecausethetranscoderandSAEsitatverysimilarpointson
theL -cross-entropyParetofrontier: thetranscoderhasanL of44.04andacross-entropyof3.35
0 0
nats,whiletheSAEhasanL of47.85andacross-entropyof3.36nats. Pythia-410Mwaschosenas
0
themodelwiththeviewthatitsfeatureswerelikelytobemoreinterestingthanthoseofGPT2-small,
whilerequiringlesscomputationalpowertodeterminetopactivatingexamplesthanPythia-1.4B
would. Layer15waschosenlargelyheuristically,becausewebelievedthatthislayerislateenough
inthemodeltocontaincomplexfeatures,whilenotsolateinthemodelthatfeaturesareprimarily
encapsulatinginformationaboutwhichtokenscomenext.
InTable1, wereferto“context-free”featuresthatinterpretablefeaturesthatseemedtofireona
singletoken(ortwotokens)regardlessofthecontextinwhichtheyappeared. Examplesoffeatures
inallfourcategories(“interpretable”,“maybeinterpretable”,“uninterpretable”,and“context-free”),
alongwiththeexactannotationusedbythehumanrater,canbefoundinFigure6.
G DetailsonSection5.2
Toobtainthede-embeddingscoresshowninFigures5and4,thefollowingmethodwasused. First,
weusedthemethodpresentedinAppendixD.3todeterminewhichMLP0transcoderfeatureshadthe
highestinput-invariantconnectionstothegivenMLP10transcoderfeaturethroughattentionhead1in
22

(a)Top-activatingexamplesforafeatureannotated
as “interpretable”. The specific annotation (b) Top-activating examples for a feature anno-
was local context feature, fires on tated as “maybe interpretable”. The specific
phrases describing short amounts of annotation was local context feature for
time. boredom? MAYBE.
(c) Top-activating examples for a feature an- (d)Top-activatingexamplesforafeatureannotated
notated as “uninterpretable”. The specific as “context-free”. The specific annotation was
annotation was " Whats" > "ADVERTISEMENT "oc" in middle of words single-token
Thanks" > "olog" NOT INTERPRETABLE. feature.
Figure6: Examplesof“feature-dashboards”usedinthefeatureinterpretationexperiments.
layer9. Specifically,forMLP0transcoderfeatureiandMLP10transcoderfeaturej,thisattribution
(cid:16) (cid:17)T (cid:16) (cid:17)T
is givenby f(0,i) W(9,1) f(10,j). For each MLP10 transcoder feature, the top tenMLP0
dec OV enc
transcoderfeatureswereconsidered. Then,foreachMLP0transcoderfeature,thede-embedding
scoreofeachYYtokenforthatMLP0featurewascomputed.Thetotalde-embeddingscoreofeachYY
tokenforanMLP10featurewascomputedasthesumofthede-embeddingscoresofthattokenover
thetoptenMLP0features,witheachde-embeddingscoreweightedbytheinput-invariantattribution
oftheMLP0feature. InFigures5and4,thede-embeddingscoreswerescaledandrecenteredin
ordertofitonthegraph.
Themeanprobabilitydifferencemetricdiscussedintheoriginalgreater-thanworkisasfollows.Given
thelogitsforeachYYtoken,computethesoftmaxovertheselogitsinordertoobtainaprobability
distributionovertheYYtokens;letp denotetheprobabilityofthetokencorrespondingtoyeary.
y
Then, the probability difference for a given prompt containing a certain input year y is given by
23

(cid:80) (cid:80)
p − p . Themeanprobabilitydifferenceisthemeanoftheprobabilitydifferences
y′>y y′ y′≤y y′
overall100prompts.
H Fullcasestudies
H.1 Classicblindcasestudies
H.1.1 Citationfeature: tc8[355]
First,wecheckedactivationsforthefirst12,800promptsinthetrainingdata.Usingthis,weidentified
thepromptindexedat(5701,37)asoneof11promptsforwhichtc8[355]activatedaboveascore
of11.
Path-basedanalysisoninputindex(5701,37)revealedcontributionsfromvarioustokens,notably
attn7[7]@35andattn5[6]@36. However,wefirstdecidedtofocusonthecurrenttoken.
Current-token features. Top de-embeddings for both tc0[9188] and tc0[16632] were all
variants of a semicolon: ;,’;,%;, and.;. We also checked tc6[11831]@-1 and found that its
topcontributingfeaturesfromlayer0weretc0[16632]andtc0[9188]: thesametwosemicolon
features. Onthebasisofthis,weconcludedthatthefinaltokenisasemicolon.
Surname features. Next we focused on attn7[7]@35. Some interpretable features with high
attributionsthroughthiscomponentincludedtc0[13196]@36(years),tc0[10109]@31(openparen-
theses), mlp8tc[355]attn7[7]attn0[1]@35 (components of last names), tc0[12584]@32: P,
andtc0[7659]@34:ck.
Input-independentinvestigationoftc6[21046]@35revealedhighcontributionsfromtc0[16382]
and tc0[5468]. feat016382 corresponded to tokens such asoglu,owski, andzyk; tc0[5468]
correspondedtotokenssuchas Burnett, Hawkins,and MacDonald. Observingthatallofthese
are(componentsof)surnames,wedecidedthattoken35waslikely(partof)asurname.
Repeatinganalysiswithprompt(6063,47). Topattributionsforthispromptonceagainidentified
tc0[9188], the semicolon feature from earlier. We filtered our computational paths to exclude
thistranscoderfeature,sincewealreadyhadahypothesisaboutwhatitwasdoing. Thisidentified
tc0[10109]@39andtc0[21019]@46astop-contributingfeatures.
Thetopde-embeddingtokensfortc0[10109]@39were (, (=,and (˜. Onthebasisofthis,we
determinedthattoken39waslikelyanopenparenthesis. Meanwhile,thetopde-embeddingtokens
fortc0[21019]@46were 1983, 1982,and 1981. Thiscausedustoconcludethattoken46was
likelyayear.
We noted that, in the previous prompt, the attribution for the year features went through
attn5[6], whereas on this prompt it went through attn2[9]. We decided to investigate
the behavior of attn5[6] on this prompt, and found that it was attributing to features
tc0[16542]@11,tc0[4205]@11,andtc0[19728]@11. Thede-embeddingresultsforthesewere
mixed: tc0[16542]werebothclose-parenthesisfeatures,whereastc0[4205]includedcitation-
relatedtokenslike Accessed, Neuroscience,and Springer.
Finalresult. Wedecidedthattc8[355]waslikelyasemicolon-in-citationsfeatureandlookedat
activatingprompts. Top-activatingpromptsincluded“Res. 15,241–247;1978). Intheirpaper,”,
“aythamah,2382;Tahdh¯ıbal-”,and“lesions(Poeck,1969;Rinn,1984). It”. Notethatthelastof
thesewasprompt(5701,37),i.e. thefirstcasestudyweconsidered.
Ingeneral,thetop-activatingfeaturescorroboratedourhypothesis,andwedidnotfindanyunrelated
prompts.Wenoticedthatmanyofthetopactivatingpromptshadacommabeforetheyearincitations,
butourcircuitanalysisneveridentifiedacommafeature.
Wecomparedtranscoderactivationsontheprompts“(Leisman,1976;”and“(Leisman1976;”and
foundtc8[355]toactivatealmostidenticallyforbothwhenallprecedingMLPswerereplacedby
transcoders(4.855and4.906,respectively)andontheoriginalmodel(12.484and12.13,respectively).
24

H.1.2 “Caught”feature: tc8[235].
First,wecheckedactivationsforthefirst12,800promptsinthetrainingdata.Usingthis,weidentified
prompt(8531,111)asoneof13promptsforwhichtc8[235]activatedaboveascoreof11.
Input(8531,111). Pathanalysisrevealedthatthisfeaturealmostexclusivelydependsonthefi-
nal token in the input. Input-independent connections to the top-contributing transcoder feature,
tc7[14382],revealedthelayer-0transcoderfeaturestc0[1636](de-embeddings: caught,aught)
tc0[5637](de-embeddings: captured, caught),tc0[3981](catch, catch)astopcontribu-
tors.
Inputs (6299,39) and (817,63). For input (6299,39), we again saw top computational paths
dependedmostlyonthefinaltoken. Thistime,weidentifiedtc7[14382]andtc0[1636]—bothof
whichwerealreadyidentifiedforthepreviousprompt—astopcontributors.
For input (6299,39) we also observed the same pattern. This caused us to hypothesize that this
featurefiresonpast-tensesynonymsof“tocatch.”
Finalresult. Topactivatingpromptsforthisfeaturewereallformsof“caught,”butthevarious
synonyms,suchas“uncovered,”werenowheretobefound.
“Caught”asparticiple. Additionally,wenoticedthat“caught”wasusedasaparticiplerather
thanafiniteverbinalltop-activatingexamples. Toexplorethis,weinvestigatedthedifferencein
activationsbetweentheprompts“Hewascaught”and“Hecaughttheball”,andfoundthattheformer
causedtc8[235]toactivatestrongly(19.97)whereasthelatteractivatedveryweakly(0.8145).
WhenwetestedthesamepromptswhilereplacingallprecedingMLPswithtranscoders,wefound
thedifferencemuchlessstark: 16.45for“Hewascaught”and9.00for“Hecaughttheball”. This
suggeststhattranscoderswerenotaccuratelymodelingthisparticularnuanceofthefeaturebehavior.
Finally,wecheckedtoppathsforcontributionsthroughthe wastokenontheprompt“Hewascaught”
toseewhetherwecouldfindanythingrelatedtothisnuanceinourcircuits. Thisanalysisrevealed
attn1[0]@2asimportant,andwereabletodiscovermildattributionstotranscoderfeatureswhose
topde-embeddingswere wasandrelatedtokens.
H.2 Restrictedblindcasestudies
Beyond asimple blind casestudy, wecarried outa numberof “restrictedblind case studies.” In
these,alloftherulesofaregularblindcasestudyapply,andadditionallyitisprohibitedtolookat
input-dependentinformationaboutlayer-0transcoderfeatures.
Sincelayer0featuresaremorecommonlysingle-tokenfeatures,andingeneralthereisalmostno
contextual information available for the MLP yet, layer 0 features tend to be substantially more
informativeaboutthetokensinthepromptthanfeaturesinotherlayersare. Thus,itisoftenpossible
toreconstructlargeportionsofthepromptjustfromthede-embeddingsofwhichlayer0transcoder
featuresareactive—and,althoughweneverlookattheseactivationsdirectly,theyarefrequently
revealedandanalyzedaspartofactivecomputationalgraphsleadingtosomedownstreamfeature.
Byomittinginput-dependentinformationaboutlayer0featuresfromouranalysis,wemustrelymore
oncircuit-levelinformation,andremainsubstantiallymoreignorantofthepromptsforactivating
examples. Note that input-independent information about layer 0 features can still be used: for
instance,wecanlookattopinput-independentconnectionstolayer0features,andthede-embeddings
forthoseaswell—attheexpenseofnotknowingwhetherthosefeaturesareactiveornot.
H.2.1 Localcontextfeature: tc8[479].
Ourfirstexampleofablindcasestudyfollowstc8[479],whichwefailtocorrectlyannotatethrough
circuitanalysis. Weincludethiscasestudyfortransparency,andasaninstructiveexampleofhow
thingscangoawryduringblindcasestudies. First,wemeasuredfeatureactivationsover12,800
promptsandidentified6promptsthatactivatedaboveathresholdof10.
25

Input (3511,64). For this prompt, path analysis revealed a lot of attention head involve-
ment from many previous tokens. For our first analysis, we chose the path mlp8tc[479]@-1
<- attn8[5]@62: 8.1 <- mlp7tc[10719]@62, since we could look at de-embeddings for
tc7[10719]@62. Top input-independent connections from tc7[10719]@62 to layer 0 were
tc0[22324]andtc0[2523],whichhad estimatedand estimateastheirtopde-embeddings,
respectively. Thus,wehypothesizedthattoken62is“estimate(d)”.
Next, we looked at the pullback of tc8[479] through attn8[5] through attn7[5]@57. This
revealed top input-independnet connections to tc0[23855] (top de-embedding tokens: spree,
havoc, frenzy),tc0[8917](tookde-embeddingtokens: amounts, quantities,amount),and
tc0[327](massive, massive, huge). Wefoundthisaspectoftheanalysistobeinconclusive.
The pullback of tc8[479] through attn8[5] through attn6[11]@57 revealed connections to
tc0[13184](total),tc0[12266]( comparable),andtc0[12610]( averaging). Thisledus
tobelievethattoken57relatestoquantities.
Wefoundthattc3[18655]wasatoptranscoderfeatureactiveonthecurrenttoken. Thisshowed
topinput-independentconnectionstotc0[11334]andtc0[5270],bothofwhichde-embeddedas
be. Thisledustohypothesizethattc8[479]featuresonphraseslike“theamount/total/averageis
estimatedtobe...”.
Input (668,122). For this prompt, most contributions once again came from previous tokens.
Thetopcontributorwasattn8[5]@121,whichhadinput-independetconnectionstotc0[12151]
( airport), tc0[8192] (pired), tc0[13184] (total), and tc0[1300] ( resulted). This was
inconclusive,butthisisthesecondtimethattc0[13184]hasappearedinde-embeddings.
Next,weinvestigatedattn8[7]@121: itconnectedtotc0[16933]( population),tc0[14006]
(kinson,rahim,LU,...),tc0[19887]( blacks),andtc0[6821]( crowds). Theseseemedrelated
togroupsofpeople,butthisanalysiswasalsoinconclusive.
Whenweinvestigatedtc4[18899]@121,topinput-idependentconnectionstolayer-0featuresin-
cludedtc0[22324],whichde-embeddedto estimatedagain. Thiswasmoreconsistentwiththe
behavioronthepreviousprompt.
To understand the current-token behavior, we looked at tc7[13166]@-1. Top input-indendent
connectionsweretc0[18204]( discrepancy)andtc0[14717]( velocity). tc1[19616]@-1
and tc3[22544]-1, both of which also contributed, each had top connections to tc0[19815]
( length). Thisledustoguessthatthispromptrelatestoestimatedlength.
Next,welookedatprevioustokens. Onefeature,tc5[10350]@119,wasconnectedtotc0[23607]
and tc0[4252], both of which de-embedded to variants of With. For the next token,
tc6[15690]@120 was connected to tc0[22463] and tc0[18052] (both a). This updated our
hypothesistosomethinglike“withanestimatedlength.”
Further back in the prompt, we saw tc4[23257]@29 (connected to tc0[12475]: remaining,
tc0[16996]: entirety).
Input (7589,89). One feature, tc7[6]@87, pulled back to tc0[22324], which de-embedded
to estimated. A following-token feature, tc1[14473], pulled back to tc0[4746] ( annual,
yearly),andthenext-tokenfeaturetc1[12852]@89,pulledbacktotc0[923]( revenue). Thus,
thispromptseemedtoendin“estimatedyearlyrevenue.”
Estimates for earlier tokens included tc4[23699]@85 (tc0[10924]: with), tc5[6568]@86
(tc0[1595]: a). Thismatchedthepatternfromearlier,whereweexpectedapromptlike“withan
estimatedlength”—butnowweexpect“withanestimatedannualrevenue.”
Lookingatthepulled-backfeaturemlp8tc[479]attn3[2]@86,noneoftheconnectionswefoundto
beveryinformative. Thisisconsistentwithpatternsobservedinothercasestudies,wherepullbacks
throughattentiontendedtobehardertointerpret.
Finalguess. Onthebasisoftheaboveexamples, weguessedthatthisfeaturefiresonprompts
like“withatotalestimated...”. Whenweviewedtopactivatingexamples,wefoundanumberof
examplesthatmatchedthispattern,especiallyamongthehighesttotalactivations. However,formany
ofthelowest-activationpromptswesawquitedifferentbehaviors. Activatingpromptsrevealedthat
26

thisisalocalcontextfeature,whichinretrospectmayhavebeenapparentthroughtheveryhigh
levelsofattentionheadinvolvementinallcircuitsweanalyzed.
H.2.2 Single-tokenAllfeature: tc8[1447]
Ananalysisofthefirst12,800promptsrevealed21featuresactivatingaboveathresholdof11. One
ofthesewasinput(3067,79). Thecomputationalpathsforthispromptrevealedallcontributions
camefromthefinaltoken.
Thetopattributionwasduetotc7[10932],withatopinput-independentconnectiontotc0[4012],
which de-embedded toAll. The next-highest was tc6[8713], which connected to tc0[6533],
whichde-embeddedto All(notetheleadingspace). Theseobservationsledustohypothesizethisis
probablyasimple,single-tokenfeaturefor“All.”
We also looked at context-based contributions by filtering out current-token features, and found
the top attributions to max out at 0.23 (compared to 3.5 from tc7[10932]@79). This was quite
low,indicatingcontextwasprobablynotveryimportant. Nevertheless,weexploredthepullbackof
tc8[1447]throughtheOVcircuitofattn4[11]@78anddiscoveredseveralseemingly-unrelated
connectionswithlowattributions. WhenwepulledbackthroughtheOVcircuitofattn1[1]@78
and attn2[0]@78, both showed input-independnt connections to features that de-embedded as
punctuationtokens. Overall,thecontextseemedtocontributelittle,excepttosuggestthattheremay
bepunctuationprecedingthisinstanceof All.
Werepeatedthisanalysiswithanotherinput,(8053,72),andfoundthesamefeaturescontributing:
tc7[10932],followedbytc6[8713]. Thisledustoconcludethisisasingle-token“All”feature.
Topactivatingexamplesconfirmedthis: thefeatureactivatedmosthighlyforAll,then All,and
finally all. Overall,thisfeatureturnedouttobequitestraightforward,anditwaseasytounderstand
itsfunctionpurelyfromtranscodercircuits.
H.2.3 Interviewfeature: tc8[6569]
Forthisfeature,wefound15outof12,800promptstoactivateaboveathresholdof16.
Input(755,122). Westartedbyexploringinput(755,122),whichrevealedseveralcontributions
fromothertokens.
We began by looking at components that contributed to the final token. The top feature
was tc7[17738], which connected to tc0[15432] (variants of interview), tc0[12425]
(variants of interviewed), and tc0[12209] (tokens like Transcript, Interview, and
rawdownloadcloneembedreportprint). The next feature, tc3[11401], was connected to
tc0[15432]andtc0[12425](sameastheprevious),aswellastc0[21414],whichde-embedded
tovariantsof spoke. Thisraisedthepossibilitythat“interview”isbeingusedasaverbinthispart
oftheprompt.
Next,weturnedourattentiontoprevioustokensinthecontext,inhopesthatthiswouldclarifythe
senseinwhich“interview”wasbeingused. Thetopattributionfortheprevioustoken(121)was
throughattn4[11]. Thede-embeddingsfortopinput-independentfeatureswereuninformative:
tc0[22216]seemedtocovervariantsofgest),whiletc0[7791]coveredvariantsofsector. For
token120,pullbacksthroughattn2[2]showedconnectionstotc0[10564]andtc0[9519],both
ofwhichde-embeddedtovariantsofIn. Thisledustobelieve“interview”wasinfactbeingusedasa
noun,e.g. “inaninterview...”
Thetopattributionfortoken119camethroughattn4[9],andshowedconnectionsto:
• tc0[625]: allegations, accusations, allegation,...,
• tc0[10661]: allegedly, purportedly, supposedly,...,and
• tc0[22588]: reportedly, rumored, stockp,....
Thenext-highestattributioncamethroughattn8[5],andshowedconnectionsto:
• tc0[4771]: Casey, Chase, depot,...,and
• tc0[5436]: didn,didn, wasn...
27

Thenext-highestwastc2[5264]@119,whichshowedconnectionsto:
• tc0[5870]: unlocks, upstairs, downstairs,...,
• tc0[14674]: saidandvariants,and
• tc0[12915]: saidandvariants
Thisledustobelievethatthisfeaturefireson“saidinaninterview”-typeprompts.
Input(1777,53). Nextwetriedanotherprompt,(1777,53). Thetopfeaturesforthecurrenttoken
wereidenticaltothepreviousexample: tc7[17738],tc3[11401],tc6[24442],andsoon.
Forthecontext,wefirstlookedatthepullbackofourfeaturethroughtheOVcircuitofattn2[2]@51.
This showed input-independent connections to tc0[10564], which once again de-embedded to
In. Nextup,attn4[9]@50. Thisfeatureconnectedtotc0[625],tc0[10661],andtc0[22588],
exactlylikebefore. Recallthatthesefeaturesde-embedto“said”and“allegedly”-typetokens.
Finally, wesawahighattributionfromamuchearliertokenviaattn8[9]@16. Thepullbackof
ourfeaturethroughthisheadshowedhighinput-independentconnectionstotc0[14048],whose
de-embeddingswereallvariantsof election.
Input(10179,90). Forourlastinput,weonceagainfoundthesametranscoderfeaturescontributing
throughthecurrenttoken. Forearliertokens,wetried:
• attn2[2]@88,findingtc0[10564](In)again;
• attn8[9]@86,findingtc0[16885],whichalsode-embeddedto electionsdespitebeinganew
feature;
• attn6[20291]@86,findingtc0[372]( told);and
• tc6[20291]@86,findingtc0[372]again.
Finalguess. Insum,wedecidedthisfeaturefiresforpromptsconveying“told/saidinaninterview.”
Topactivatingexamplescorroboratedthis,withoutanynotabledeviationsfromthispattern.
H.2.4 Fourmorerestrictedblindcasestudies
WepresenttheresultsoffourmorerestrictedblindcasestudiesinTable3.Intheinterestofconserving
space,onlytheresultsofthesecasestudiesarepresented. However,inthesupplementalmaterial
attachedtothissubmission,theoriginalJupyterNotebooksinwhichthecasestudieswerecarriedout
areprovided.
Table3: Theresultsoffourmorerestrictedblindcasestudies.
Feature Finalhypothesis Actualinterpretation Outcome
tc8[9030] Fires on biologywhen in Fires on scientific subjects Failure
thecontextofbeingasubject of study like chemistry,
ofstudy psychology, biology,
economics
tc8[4911] Fires on though or Fires on though or Success
althoughinthebeginning althoughinthebeginning
ofaclause ofaclause
tc8[6414] Largely uninterpretable fea- Largely uninterpretable fea- Success
turethatsometimesfireson turethatsometimesfireson
Cyrillictext Cyrillictext
tc8[2725] Firesonphrasesaboutnotof- Firesonphrasesaboutnotof- Mostlyasuccess
feringthingsornotproviding feringthingsornotproviding
things. (Asastretch: particu- things,ingeneral
larlyinlegalesecontext?)
28

Table4: Theresultsofallblindcasestudies.
Feature Type Finalhypothesis Actualinterpretation Outcome
tc8[355] Blind Fires on semicolons in the Fires on semicolons in the Success
contextofacademiccitations contextofacademiccitations
tc8[1447] RestrictedBlind Single-token“All”feature Single-token“All”feature Success
tc8[6569] RestrictedBlind Firesonpromptsconveying Firesonpromptsconveying Success
“told/saidinaninterview” “told/saidinaninterview”
tc8[4911] RestrictedBlind Fires on though or Fires on though or Success
althoughinthebeginning althoughinthebeginning
ofaclause ofaclause
tc8[6414] RestrictedBlind Largely uninterpretable fea- Largely uninterpretable fea- Success
turethatsometimesfireson turethatsometimesfireson
Cyrillictext Cyrillictext
tc8[235] Blind Fires on past-tense syn- Firesonformsof“caught” Mostlyasuccess
onymsof“tocatch”
tc8[2725] RestrictedBlind Firesonphrasesaboutnotof- Firesonphrasesaboutnotof- Mostlyasuccess
feringthingsornotproviding feringthingsornotproviding
things. (Asastretch: particu- things,ingeneral
larlyinlegalesecontext?)
tc8[479] RestrictedBlind Firesonpromptsresembling Alocalcontextfeature Failure
“withatotalestimated...”
tc8[9030] RestrictedBlind Fires on biologywhen in Fires on scientific subjects Failure
thecontextofbeingasubject of study like chemistry,
ofstudy psychology, biology,
economics
29