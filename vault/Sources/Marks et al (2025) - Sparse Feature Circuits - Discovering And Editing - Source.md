---
title: "Sparse Feature Circuits: Discovering And Editing Interpretable Causal Graphs In Language Models - Source"
type: "source"
source_type: "pdf_text"
added: "2026-02-26"
---

PublishedasaconferencepaperatICLR2025
SPARSE FEATURE CIRCUITS: DISCOVERING
AND EDITING INTERPRETABLE CAUSAL GRAPHS
IN LANGUAGE MODELS
SamuelMarks∗ CanRager EricJ.Michaud
NortheasternUniversity Independent MIT
YonatanBelinkov DavidBau AaronMueller*
Technion–IIT NortheasternUniversity NortheasternUniversity
ABSTRACT
We introduce methods for discovering and applying sparse feature circuits.
These are causally implicated subnetworks of human-interpretable features for
explaininglanguagemodelbehaviors. Circuitsidentifiedinpriorworkconsistof
polysemanticand difficult-to-interpretunits like attentionheads orneurons, ren-
deringthemunsuitableformanydownstreamapplications.Incontrast,sparsefea-
turecircuitsenabledetailedunderstandingofunanticipatedmechanismsinneural
networks. Because they are based on fine-grained units, sparse feature circuits
are useful for downstream tasks: We introduce SHIFT, where we improve the
generalizationofaclassifierbyablatingfeaturesthatahumanjudgestobetask-
irrelevant. Finally, we demonstrate an entirely unsupervised and scalable inter-
pretability pipeline by discovering thousands of sparse feature circuits for auto-
maticallydiscoveredmodelbehaviors.
1 INTRODUCTION
Thekeychallengeofinterpretabilityresearchistoscalablyexplainthemanyunanticipatedbehav-
iorsofneuralnetworks(NNs). MuchrecentworkexplainsNNbehaviorsintermsofcoarse-grained
modelcomponents,forexamplebyimplicatingcertaininductionheadsinin-contextlearning(Ols-
son et al., 2022) or MLP modules in factual recall (Meng et al., 2022; Geva et al., 2023; Nanda
et al., 2023, inter alia). However, such components are generally polysemantic (Elhage et al.,
2022) and hard to interpret, making it difficult to apply mechanistic insights to downstream ap-
plications. Ontheotherhand,priormethodsforanalyzingbehaviorsintermsoffine-grainedunits
(Kimetal.,2018;Belinkov,2022;Geigeretal.,2023;Zouetal.,2023)attempttofitmodelinternals
toresearcher-specifiedmechanistichypothesesusingresearcher-curateddata. Theseapproachesare
not well-suited to the many cases where researchers cannot anticipate ahead of time how models
internallyimplementtheirsurprisingbehaviors.
We propose to explain model behaviors using fine-grained components that play narrow, inter-
pretable roles. Doing so requires us to address two challenges: First, we must identify an appro-
priatefine-grainedunitofanalysis,sinceobviouschoiceslikeneurons1arerarelyinterpretable,and
unitsdiscoveredviasupervisedmethodslikelinearprobingrequirepre-existinghypotheses(Mueller
etal.,2024). Second,wemustaddressthescalabilityproblemposedbysearchingforcausalcircuits
overalargenumberoffine-grainedunits.
WeleveragerecentprogressindictionarylearningforNNinterpretability(Brickenetal.,2023;Cun-
ninghametal.,2024)totacklethefirstchallenge. Namely,weusesparseautoencoders(SAEs)to
identifydirectionsinLMlatentspaceswhichrepresenthuman-interpretableconcepts. Then,toad-
dressthescalabilitychallenge,weemploylinearapproximations(Sundararajanetal.,2017;Nanda,
∗Correspondencetos.marks@northeastern.eduandaa.mueller@northeastern.edu.
1Weuse“neuron”torefertoabasis-aligneddirectioninanLM’slatentspace(notnecessarilyprecededby
anonlinearity).
1
5202
raM
72
]GL.sc[
3v74691.3042:viXra

PublishedasaconferencepaperatICLR2025
Data
Contrastive Pairs
Get feature circuit. Interpret circuit. Debug if desired.
§3 The boy near the teacher has
The boys near the teacher have m §3 m §3,4,5 m §4
Classification Data
§4 His research is in … Professor
She worked in the OR … Nurse
Auto-discovered Behaviors
§5
Part 1, Part 2, Part 3, Part 4
Figure1: Overview. Givencontrastiveinputpairs, classificationdata, orautomaticallydiscovered
modelbehaviors, wediscovercircuitscomposedofhuman-interpretablesparsefeaturestoexplain
theirunderlyingmechanisms. Wethenlabeleachfeatureaccordingtowhatitactivatesonorcauses
themodeltopredict. Finally,ifdesired,wecanablatespuriousfeaturesoutofthecircuittomodify
howthesystemgeneralizes.
2022; Syed et al., 2023) to efficiently identify SAE features which are most causally implicated
in model behaviors, as well as connections between these features. The result is a sparse fea-
turecircuitwhichexplainshowmodelbehaviorsariseviainteractionsamongfine-grainedhuman-
interpretableunits.
Sparsefeaturecircuitscanbeproductivelyusedindownstreamapplications. Weintroduceatech-
nique,SparseHuman-InterpretableFeatureTrimming(SHIFT; §4),whichshiftsthegeneralization
ofanLMclassifierbysurgicallyremovingsensitivitytounintendedsignals. Unlikepreviouswork
onspuriouscueremoval—whichisolatesspurioussignalsusingdisambiguatingdata—SHIFTiden-
tifies unintended signals using interpretability and human judgement. We thus showcase SHIFT
by debiasing a classifier in a worst-case setting, where an unintended signal (gender) is perfectly
predictiveoftargetlabels(profession).
Finally,wedemonstrateourmethod’sscalabilitybyautomaticallydiscoveringthousandsofnarrow
LMbehaviors—forexample,predicting“to”asaninfinitiveobjectorpredictingcommasindates—
with the clustering approach of Michaud et al. (2023), and then automatically discovering feature
circuitsforthesebehaviors(§5).
Ourcontributionsaresummarizedasfollows(Figure1):
1. Ascalablemethodtodiscoversparsefeaturecircuits. Wevalidateourmethodbydiscov-
eringandevaluatingfeaturecircuitsonasuiteofsubject-verbagreementtasks.
2. SHIFT,atechniqueforremovingaLMclassifier’ssensitivitytounintendedsignals,even
withoutdatathatisolatethesesignals.
3. Afully-unsupervisedpipelineforcomputingfeaturecircuitsforthousandsofautomatically
discoveredLMbehaviors,viewableatfeature-circuits.xyz.
Wereleasecode,dataandautoencodersatgithub.com/saprmarks/feature-circuits.
2 FORMULATION
Feature disentanglement with sparse autoencoders. A fundamental challenge in NN inter-
pretabilityisthatindividualneuronsarerarelyinterpretable(Elhageetal.,2022). Therefore,many
interpretability researchers have recently turned to sparse autoencoders (SAEs), an unsupervised
technique for identifying a large number of interpretable NN latents (Cunningham et al., 2024;
Brickenetal.,2023;Templetonetal.,2024;Rajamanoharanetal.,2024a;b). Givenamodelcom-
ponentwithlatentspaceRdandanactivationx∈Rd,anSAEcomputesadecomposition
(cid:88)
dSAE
x=xˆ+ϵ(x)= f (x)v +b+ϵ(x) (1)
i i
i=1
intoanapproximatereconstructionxˆ asasparsesumoffeaturesv andanSAEerrortermϵ(x) ∈
i
Rd. Hered isthewidthoftheSAE,thefeaturesv ∈Rdareunitvectors,thefeatureactivations
SAE i
f (x) ≥ 0areasparsesetofcoefficients, andb ∈ Rd isabias. SAEsaretrainedonanobjective
i
2

PublishedasaconferencepaperatICLR2025
whichpromoteshavingasmallreconstructionerror∥x−xˆ∥ whileusingonlyasparsesetoffeature
2
activations f (x). Rather than discard the error terms ϵ for the purposes of circuit discovery, our
i
methods handle them gracefully by incorporating them into our sparse feature circuits; this gives
a principled decomposition of model behaviors into contributions from interpretable features and
errorcomponentsnotyetcapturedbyourSAEs.
Inthiswork,weleveragethefollowingsuitesofSAEs:
• A suite of SAEs we train for each sublayer (attention layer, MLP, residual stream, and
embeddings) of Pythia-70M (Biderman et al., 2023). We closely follow Bricken et al.
(2023),usingaReLU-linearencoderf andsparsedimensiond =64×dandtraining
i SAE
theSAEstominimizeacombinationofanL2reconstrutionlossandL1regularizationterm
whichpromotessparsity. DetailsaboutourPythiaSAEsandtheirtrainingcanbefoundin
AppendixB.1.
• The open source Gemma Scope SAEs (Lieberum et al., 2024) available for all sublay-
ers(excludingembeddings)oftheopen-weightsGemma-2-2Bmodel(Teametal.,2024).
TheseSAEsuseaJump-ReLU-linearencoderandd =8×d. DetailsabouttheGemma
SAE
ScopeSAEscanbefoundinAppendixB.2.
ScalablytrainingbetterSAEsisanactiveareaofresearch,asillustratedbythereadyavailabilityof
open-source SAEs (Gao et al., 2024; Lieberum et al., 2024; Lin & Bloom, 2023). Thus, our goal
is to—given a suite of trained SAEs—scalably apply them to understand NN behaviors; we treat
scalingtheSAEsthemselvesasout-of-scope.
Attributingcausaleffectswithlinearapproximations. Letmbeareal-valuedmetriccomputed
viaacomputationalgraph(e.g., aNN);letarepresentanodeinthisgraph. Followingpriorwork
(Vig et al., 2020; Finlayson et al., 2021), we quantify the importance of a on a pair of inputs
(x ,x )viaitsindirecteffect(IE;Pearl,2001)onm:
clean patch
IE(m;a;x ,x )=m(x |do(a=a ))−m(x ). (2)
clean patch clean patch clean
Here,a isthevaluethatatakesinthecomputationofm(x ),andm(x |do(a = a ))
patch patch clean patch
denotesthevalueofmwhencomputingm(x )butinterveninginthecomputationofmbymanu-
clean
allysettingatoa .Forexample,giveninputsx =“Theteacher”andx =“Theteachers,”
patch clean patch
we have metric m(x) = logP(“are”|x)−logP(“is”|x), the log probability difference output by
the LM. Then if a is the activation of a particular neuron, a large value of IE(m;a;x ,x )
clean patch
indicatesthattheneuronishighlyinfluentialonthemodel’sdecisiontooutput“is”vs.“are”onthis
pairofinputs.
WeoftenwanttocomputeIEsforaverylargenumberofmodelcomponentsa∈Rd,whichcannot
be done efficiently with (2). We thus employ linear approximations to (2) that can be computed
formanyainparallel. Thesimplestsuchapproximation,attributionpatching(Nanda,2022;Syed
etal.,2023;Krama´retal.,2024),employsafirst-orderTaylorexpansion
IˆE (m;a;x ,x )= ∇ m| (a −a ) (3)
atp clean patch a a=aclean patch clean
whichestimates(2)foreveryainparallelusingonlytwoforwardandonebackwardpass.
To improve the quality of the approximation, we can instead employ a more expensive but more
accurateapproximationbasedonintegratedgradients(Sundararajanetal.,2017;Hannaetal.,2024):
(cid:32) (cid:33)
1 (cid:88)
IˆE (m;a;x ,x )= ∇ m| (a −a ) (4)
ig clean patch N a αaclean+(1−α)apatch patch clean
α
where the sum in (4) ranges over N = 10 equally-spaced α ∈ {0, 1,...,N−1}. This cannot be
N N
doneinparallelfortwonodeswhenoneisdownstreamofanother, butcanbedoneinparallelfor
arbitrarilymanynodeswhichdonotdependoneachother. Thustheadditionalcostofcomputing
IˆE overIˆE scaleslinearlyinN andtheserialdepthofm’scomputationgraph.
ig atp
Theabovediscussionappliestothesettingwherewehaveapairofcleanandpatchinputs,andwe
wouldliketounderstandthateffectofpatchingaparticularnodefromitscleantopatchvalues. But
in some settings (e.g., §4, 5), we have only a single input x. In this case, we instead use a zero-
ablation,usingtheindirecteffectIE(m;a;x) = m(x|do(a = 0))−m(x)fromsettingato0. We
getthemodifiedformulasforIˆE(m;a;x)from(3)and(4)byreplacingawith0.
3

PublishedasaconferencepaperatICLR2025
SAE feature x m
SAE error
a1 a2
b1 b2
Submodule ϵ1 ϵ2
1 Cache activations and metric. 2 Backpropagate. 3 Compute effects. 4 Compute and
Store gradients. Filter nodes. filter edges.
m = log p(have) – log p(has)
m m ∇ a1 m m ∇ ϵ1 m m m
∇ m ∇ m
a2 ϵ2
a 2 b 2 ϵ 2 a 2 b 2 ϵ 2 a 2 b 2 ϵ 2 a 2 b 2 a 2 b 2
a 1 b 1 ϵ 1 a 1 b 1 ϵ 1 a 1 b 1 ϵ 1 b 1 ϵ 1 b 1 ϵ 1
IÊ(a,m)=∇am⋅( aa − aa )
x = The teacher x = The teachers IÊ(a,m)>TN
Figure2: Overviewofourmethod. WeviewourmodelasacomputationgraphthatincludesSAE
featuresanderrors. Wecacheactivations(Step1)andcomputegradients(Step2)foreachnode. We
thencomputeapproximateindirecteffectswithEq.(3;shown)or(4)andfilteraccordingtoanode
thresholdT (Step3). Wesimilarlycomputeandfilteredges(Step4);seeApp.A.1.
N
3 SPARSE FEATURE CIRCUIT DISCOVERY
3.1 METHOD
SupposewearegivenanLMM,SAEsforvarioussubmodulesofM (e.g.,attentionoutputs,MLP
outputs, and residual stream vectors, as in §2), a dataset D consisting either of contrastive pairs
(x ,x ) of inputs or of single inputs x, and a metric m that depends on M’s output when
clean patch
processingdatafromD. Forexample,Figure2showsthecasewhereD consistsofpairsofinputs
whichdifferinnumber,andmisthelogprobabilitydifferencebetweenM outputtingtheverbform
thatiscorrectforthepatchvs.cleaninput.
ViewingSAEfeaturesaspartofthemodel.Akeyideaunderpinningourmethodisthat,byapply-
ingthedecomposition(1)tovarioushiddenstatesxintheLM,wecanviewthefeatureactivations
f and SAE errors ϵ as being part of the LM’s computation. We can thus represent the model as
i
a computation graph G where nodes correspond to feature activations or SAE errors at particular
tokenpositions.
ApproximatingtheIEofeachnode. LetIˆEbeoneofIˆE orIˆE (see§2). Thenforeachnode
atp ig
ainGandinputx ∼ D,wecomputeIˆE(m;a;x);wethenaverageoverx ∼ Dtoproduceascore
IˆE(m;a)andfilterfornodeswith|IˆE(m;a)|>T forsomechoiceT ofnodethreshold.
N N
Consistent with prior work (Nanda, 2022; Krama´r et al., 2024), we find that IˆE accurately esti-
atp
mates IEs for SAE features and SAE errors, with the exception of nodes in the layer 0 MLP and
earlyresidualstreamlayers, whereIˆE underestimatesthetrueIE.WefindthatIˆE significantly
atp ig
improves accuracy over IˆE for these components, so we use it in our experiments below. See
atp
AppendixHformoreinformationaboutlinearapproximationquality.
Approximating the IE of edges. Using an analogous linear approximation, we also compute the
average IE of edges in the computation graph. Although the idea is simple, the mathematics are
somewhatinvolved,sowerelegatethedetailstoApp.A.1. AftercomputingtheseIEs,wefilterfor
edgeswithabsoluteIEexceedingsomeedgethresholdT .
E
Aggregationacrosstokenpositionsandexamples. Fortemplaticdatawheretokensinmatching
positionsplayconsistentroles(see§3.2,3.3),wetakethemeaneffectofnodes/edgesacrossexam-
ples. For non-templatic data (§4, 5) we first sum the effects of corresponding nodes/edges across
tokenpositionbeforetakingtheexample-wisemean. SeeApp.A.2.
4

PublishedasaconferencepaperatICLR2025
Structure Examplecleaninput Exampleoutput
Simple Theparents p(is)−p(are)
WithinRC Theathletethatthemanagers p(likes)−p(like)
AcrossRC Theathletethatthemanagerslike p(do)−p(does)
AcrossPP Thesecretariesnearthecars p(has)−p(have)
Table1: Examplecleaninputsxandoutputsmforsubject-verbagreementtasks.
1 features
features_wo_errs
0.8 features_wo_some_errs neurons
0.6
0.4
0.2
0 0 500 1000 1500
Nodes
ssenlufhtiaF
ssenlufhtiaF
1
features
0.8 features_wo_errs
features_wo_some_errs 0.6 neurons
0.4
0.2
0
0 50 100 150 200 250 300
Nodes
ssenlufhtiaF
Faithfulness of C Completeness of C (Faithfulness of M \ C)
1 features
features_wo_errs
features_wo_some_errs 0.8 neurons
0.6
0.4
0.2
0
−0.2
50 100 150 200 250 300
Nodes
ssenlufhtiaF
Feature circuit
Feature circuit w/o SAE errors
Feature circuit w/o attention/MLP SAE errors Neuron circuit
1
features
0.8 features_wo_errs
features_wo_some_errs
0.6 neurons
0.4
0.2
0
0 500 1000 1500 2000 2500 3000
Nodes
ssenlufhtiaF
M Pythia-70
1 features
features_wo_errs
0.8 features_wo_some_errs
ma-2-2B
0.6
neurons
Ge m 0.4
0.2
0
0 5k 10k 15k 20k 25k 30k
Nodes Nodes
ssenlufhtiaF
Figure3: Faithfulnessandcompletenessscoresforcircuits,measuredonheld-outdata. Faintlines
correspond to the structures from Table 1, with the average across structures in bold. The ideal
faithfulnessforcircuitsis1,whiletheidealcompletenessis0.
Practical considerations. Various practical difficulties arise for efficiently computing the gradi-
ents needed by our method. We solve these using a combination of stop gradients, pass-through
gradients,andtricksforefficientJacobian-vectorproductcomputation;seeApp.A.3.
3.2 DISCOVERINGANDEVALUATINGSPARSEFEATURECIRCUITSFORSUBJECT-VERB
AGREEMENT
Toevaluateourmethod,wediscoversparsefeaturecircuits(henceforth,featurecircuits)onPythia-
70MandGemma-2-2Bforfourvariantsofthesubject-verbagreementtask(Table1). Specifically,
we adapt data from Finlayson et al. (2021) to produce datasets consisting of contrastive pairs of
inputs that differ only in the grammatical number of the subject; the model’s task is to choose the
appropriateverbinflection.
We evaluate circuits for interpretability, faithfulness, and completeness. For each criterion, we
compare to neuron circuits discovered by applying our methods with neurons in place of sparse
features; inthissetting,therearenoerrortermsϵ. Whenevaluatingfeaturecircuitsforfaithfuless
and completeness, we use a test split of our dataset, consisting of contrastive pairs not used to
discoverthecircuit.
Interpretability. For Pythia SAEs, we asked human crowdworkers to rate the interpretability of
randomfeatures,randomneurons,featuresfromourfeaturecircuits,andneuronsfromourneuron
circuits. Crowdworkersratedsparsefeaturesassignificantlymoreinterpretablethanneurons,with
features that participate in our circuits also being more interpretable than randomly sampled ones
(App.F).ThisreplicatespriorfindingsthatSAEfeaturesaresubstantiallymoreinterpretablethan
neurons(Brickenetal.,2023). ForGemma-2SAEs,wereferthereadertoLieberumetal.(2024),
which finds the interpretability of these SAEs’ features to be on par with those trained via other
state-of-the-arttechniques.
Faithfulness. GivenacircuitC andmetricm,letm(C)denotetheaveragevalueofmoverinputs
fromDwhenrunningourmodelwithallnodesoutsideofC mean-ablated,i.e.,settotheiraverage
5

PublishedasaconferencepaperatICLR2025
value over data from D.2 We then measure the faithfulness of a circuit as m(C)−m(∅), where
m(M)−m(∅)
∅ denotes the empty circuit and M denotes the full model. Intuitively, this metric captures the
proportionofthemodel’sperformanceourcircuitexplains,relativetomeanablatingthefullmodel
(whichrepresentsthe“prior”performanceofthemodelwhenitisgiveninformationaboutthetask,
butnotaboutspecificinputs).
Wefindthatcomponentsinearlymodellayersaretypicallyinvolvedinprocessingspecifictokens.
Inpractice,theinputsinthetrainsplitofourdataset(usedtodiscoverthecircuit)andthetestsplit
(for evaluation) do not contain identical tokens, making it difficult to evaluate the quality of early
segmentsofourcircuit. Thus,weignorethefirst1/3ofourcircuit,andonlyevaluatethelatter2/3.
WeplotfaithfulnessforfeaturecircuitsandneuroncircuitsaftersweepingovernodethresholdsT
N
(Fig.3). Wefindthatsmallfeaturecircuitsexplainalargeproportionofmodelbehavior: themajor-
ityofperformanceinPythia-70M,resp. Gemma-2-2Bisexplainedbyonly100,resp. 500nodes. In
contrast,around1500,resp. 50000neuronsarerequiredtoexplainhalftheperformance. However,
asSAEerrornodesarehigh-dimensionalandcoarse-grained,theycannotbefairlycomparedtoneu-
rons;wethusalsoplotthefaithfulnessoffeaturecircuitswithallSAEerrornodesremoved,orwith
allattentionandMLPerrornodesremoved. Unsurprisingly,wefindthatremovingresidualstream
SAEerrornodesseverelydisruptsthemodelandcurtailsitsmaximumperformance;removingMLP
andattentionerrornodesislessdisruptive.
Completeness. Aretherepartsofthemodelbehaviorthatourcircuitfailstocapture? Wemeasure
thisasthefaithfulnessofthecircuit’scomplementM\C(Fig.3).Weobservethatwecaneliminate
themodel’staskperformancebyablatingonlyafewnodesfromourfeaturecircuits, andthatthis
is true even when we leave all SAE errors in place. In contrast, it takes hundreds (for Pythia) or
thousands(forGemma)ofneuronstoachievethesameeffect.
3.3 CASESTUDY: SUBJECT-VERBAGREEMENTACROSSARELATIVECLAUSE
We find that inspecting small feature circuits produced by our technique can provide insights into
howPythia-70MandGemma-2-2Barriveatobservedbehaviors.Toillustratethis,wepresentacase
studyofrelativelysmallfeaturecircuitsforsubject-verbagreementacrossarelativeclause(RC).
Tokeepthenumberofnodesweneedtoannotatemanageable,wetuneournodethresholdtopro-
duceasmallcircuitwithfaithfulness> 0.2. ForPythia,thisresultsinacircuitwith86nodesand
faithfulness 0.21; for Gemma we study a circuit with 223 nodes and faithfulness 0.21. We sum-
marize these circuits in Figure 4; the full circuits (as well as small circuits for other subject-verb
agreementtasks)canbefoundinApp.C.1. WedepictSAEfeatureswithrectanglesandSAEerrors
withtriangles.
Our circuits depict interpretable algorithms wherein both models of study select appropriate verb
forms via two pathways. The first pathway consists of features which detect the number of the
main subject and then generically promote matching verb forms. The second pathway begins the
same,butmovestherelevantnumberinformationtotheendoftherelativeclausebyusingPP/RC
boundarydetectors.Gemma2alsousesnounphrase(NP)numbertrackers,whichdetectthenumber
ofthenounthatheadsanNPandremainactiveonalltokensuntiltheendoftheNP;thesepromote
matchingverbformsateachposition,butespeciallyatthelasttokenofanNP.
Wefindsignificantoverlapbetweenthiscircuitandthecircuitwediscoveredforagreementacrossa
prepositionalphrase,withPythia-70MandGemma-2-2Bhandlingthesesyntacticallydistinctstruc-
turesinamostlyuniformway. InaccordancewithFinlaysonetal.(2021),wefindlessoverlapwith
ourcircuitsforsimpleagreementandwithinRCagreement(AppendixC.1).
4 APPLICATION: REMOVING UNINTENDED SIGNALS FROM A CLASSIFIER
WITHOUT DISAMBIGUATING LABELS
NN classifiers often rely on unintended signals—e.g., spurious features. Nearly all prior work on
mitigatingthisproblemreliesonaccesstodisambiguatinglabeleddatainwhichunintendedsignals
are less predictive of labels than intended ones. However, some tasks have structural properties
2FollowingWangetal.(2023),weablatefeaturesbysettingthemtotheirmeanposition-specificvalues.
6

PublishedasaconferencepaperatICLR2025
has/have
Verb form
discriminators
Embeddings, layer 0-4 MLP, resid Layers 2-3 attn, MLP, resid
PP/RC end detection
Noun number PP/RC detection
detection
5 4 16 5
48 8
Layers 4-5 attn, resid
The girl/girls that the teacher sees
(a)
has/have
Layers 16–25
Verb form
attn, MLP, resid
discriminators
Layers 11–18 resid PP/RC end detectors
Layers 16–25
NP number trackers Layers 11–17 resid
82 attn, MLP, resid
NP number trackers
Layer 0-22 MLP, resid 4 3 4 18
Noun number 3 3 NP number trackers
detectors PP/RC detectors
14 12
39 1 33 7
Layers 5–23 attn, MLP, resid
Layers 0–17 attn, MLP, resid
The girl/girls that the teacher sees
(b)
Figure4:SummaryofPythia’s(a)andGemma2’s(b)circuitsforagreementacrossRC(fullcircuits
inApp.C.1). Themodelsdetectthenumberofthesubject. Then,theydetectthestartofaPP/RC
modifying the subject. Verb form discriminators promote particular verb inflections (singular or
plural). Gemma2additionallyusesseparatefeaturestotrackthenumberofthenounthatheadsthe
currentnounphrase. Squaresshownumberoffeaturenodesinthegroupandtrianglesshownumber
ofSAEerrornodes,withtheshadingindicatingthesumofIˆEtermsacrossnodesinthegroup. As
wecannotdirectlyinterpretthetriangles,werelyontheirpositionsorinclusioninothergroupsto
labelthem. Ifthelabelisambiguous,weleavethetrianglesoutsidetheboxes.
whichdisallowthisassumption. Forexample,inputsfordifferentclassesmightcomefromdifferent
datasources(Zechetal.,2018). Additionally,somehaveraisedconcerns(Ngoetal.,2024;Casper
etal.,2023)thatsophisticatedLMstrainedwithhumanfeedback(Christianoetal.,2023)insettings
witheasy-to-harddomainshift(Burnsetal.,2023;Haseetal.,2024)willbemisalignedbecause,in
thesesettings,“overseerapproval”and“desirablebehavior”areequallypredictiveoftrainingreward
labels. Morefundamentally,theproblemwithunintendedsignalsisthattheyareunintended—not
theyareinsufficientlypredictive—andwewouldlikeourmethodstoreflectthis.
WethusproposeSpuriousHuman-interpretableFeatureTrimming(SHIFT),whereahumaninspects
aclassifier’sfeaturecircuitandremovesfeatureswhichtheyjudgetobetask-irrelevant. Weshow
thatSHIFTremovessensitivitytounintendedsignalswithoutaccesstodisambiguatinglabeleddata,
orevenwithoutknowingwhatthesignalsareaheadoftime.
Method. Suppose we are given labeled training data D = {(x ,y )}; an LM-based classifier C
i i
trainedonD;andSAEsforvariouscomponentsofC. ToperformSHIFT,we:
1. Apply the methods from §3 to compute a feature circuit that explains C’s accuracy on
inputs(x,y)∼D(e.g.,usingmetricm=−logC(y|x)).
2. Manuallyinspectandevaluatefortask-relevancyeachfeatureinthecircuitfromStep1.
3. AblatefromC featuresjudgedtobetask-irrelevanttoobtainaclassifierC′.
4. (Optional)Furtherfine-tuneC′ondatafromD.
Step3removestheclassifier’sdependenceonunintendedsignalswecanidentify, butmaydisrupt
theclassifier’sperformancefortheintendedsignal.Step4canbeusedtorestoresomeperformance.
7

PublishedasaconferencepaperatICLR2025
Pythia-70M Gemma-2-2B
Method ↑Profession ↓Gender ↑Worstgroup ↑Profession ↓Gender ↑Worstgroup
Original 61.9 87.4 24.4 67.7 81.9 18.2
CBP 83.3 60.1 67.7 90.2 50.1 86.7
Random 61.8 87.5 24.4 67.3 82.3 18.0
SHIFT 88.5 54.0 76.0 76.0 51.5 50.0
SHIFT+retrain 93.1 52.0 89.0 95.0 52.4 92.9
Neuronskyline 75.5 73.2 41.5 65.1 84.3 5.6
Featureskyline 88.5 54.3 62.9 80.8 53.7 56.7
Oracle 93.0 49.4 91.9 95.0 50.6 93.1
Table2: Accuraciesonbalanceddatafortheintendedlabel(profession)andunintendedlabel(gen-
der). “Worstgroupaccuracy”referstowhicheverprofessionaccuracyislowestamongmaleprofes-
sors,malenurses,femaleprofessors,femalenurses.
Experimental setup. We illustrate SHIFT using the Bias in Bios dataset (BiB; De-Arteaga et al.,
2019).BiBconsistsofprofessionalbiographies,andthetaskistoclassifyanindividual’sprofession
based on their biography. BiB also provides labels for a spurious feature: gender. We subsample
BiBtoproducetwosetsoflabeleddata:
• The ambiguous set, consisting of bios of male professors (labeled 0) and female nurses
(labeled1).
• Thebalancedset,consistingofanequalnumberofbiosformaleprofessors,malenurses,
female professors, and female nurses. These data carry profession labels (the intended
signal)andgenderlabels(theunintendedsignal).
The ambiguous set represents a worst-case scenario: the unintended signal is perfectly predictive
of training labels. Given only access to the ambiguous set, our task is to produce a profession
classifierwhichisaccurateonthebalancedset.
WeadaptPythia-70MandGemma-2-2Bintoclassifiersbytraininglinearclassificationheadswith
the ambiguous set; see App. E.1 for probe training details. We then discover feature circuits for
theseclassifiersusingthezero-ablationvariantdescribedin§3.1;thePythiacircuitcontains67fea-
tures,andtheGemmacircuitcontains46.WemanuallyinterpreteachfeatureusingtheNeuronpedia
interface (Lin & Bloom, 2023), which displays maximally activating dataset exemplars on a large
textcorpus,asthefeatures’directeffectsonoutputlogits. Wejudge55ofthePythiafeaturesand
43oftheGemmafeaturestobetask-irrelevant—e.g.,featuresthatpromotefemale-associatedlan-
guageinbiographiesofwomen,asinFigure19(seeApp.Dformoreexamplesfeatures). Although
thisinterpretabilitystepusesadditionalunlabeleddata,weemphasizethatweneveruseadditional
labeleddata(orevenadditionalunlabeledclassificationdata).
ToapplySHIFT,wezero-ablatetheseirrelevantfeatures. Finally,weretrainthelinearclassification
head with the ambiguous set using activations extracted from the ablated model. We evaluate all
accuraciesonthebalancedset.
Baselinesandskylines. TocontextualizetheperformanceofSHIFT,wealsoimplement:
• SHIFTwithneurons. PerformSHIFT,butusingneuronsinsteadofSAEfeatures.
• ConceptBottleneckProbing(CBP),adaptedfromYanetal.(2023)(originallyformulti-
modaltext/imagemodels). CBPworksbytrainingaprobetoclassifyinputsxgivenaccess
only to a vector of affinities between the LM’s representation of x and various concept
vectors. SeeApp.E.2forimplementationdetails.
• Random feature ablations. Perform SHIFT, but using (the same number of) randomly
selectedSAEfeaturesinsteadoffeaturesselectedbyahumanannotator.
• Feature skyline. Instead of relying on human judgement to evaluate whether a feature
shouldbeablated,wezero-ablatethe55(forPythia)or43(forGemma)featuresfromour
circuitthataremostcausallyimplicatedinspuriousfeatureaccuracyonthebalancedset.
• Neuronskyline. Thesameasthefeatureskyline,butmean-ablating55or43neurons.
• Oracle. Aclassifiertrainedonground-truthlabelsonthebalancedset.
Results. We find (Table 2) that SHIFT almost completely removes the classifiers’ dependence on
gender information for both models. In the case of Gemma (but not Pythia), the feature ablations
8

PublishedasaconferencepaperatICLR2025
Cluster 382: Incrementing sequences Cluster 475: “to” as infinitive object
var input = [1, 2, 3, 4, 5, 6, 7, 8 At issue, whether the defendant should be allowed to
Step 1. Download the latest CompsNY 3.49 Full British Prime Min David Cameron says in televised remarks he would like Britain to
Step 2. Double click the Setup file and follow the prompts […]
Step 3. After the main install closes, click OK […] Reader bloggers are asked to
Step 4
Example features involved: Example features involved:
Succession Narrow induction Objects which can precede Other words which precede
Chapter 1 A, B, C A3 … A → 3 or III or 4 … object complements infinitive objects
Chapter 2
Chapter 3 I, II, III, IV A7 … A → 7 or vii or 8 … Direct the user to It’s up to you to According to This infection leads to
Figure5: Exampleclustersandfeatureswhichparticipateintheircircuits(seeApp.C.3forthefull
circuits). Featuresareactiveontokensshadedinblueandpromotetokensshadedinred. (left)An
examplenarrowinductionfeaturerecognizesthepatternA3...Aandcopiesinformationfromthe
3token.ThiscomposeswithasuccessionfeaturetoimplementthepredictionA3...A→4.(right)
Onefeaturepromotes“to”afterwordswhichcantakeinfinitiveobjects. Aseparatefeatureactivates
onobjectsofverbsorprepositionsandpromotes“to”asanobjectcomplement.
damagemodelperformance;however,thisperformanceisrestored(withoutreintroducingthebias)
byfurthertrainingontheambiguousset.ComparingSHIFTwithoutretrainingtothefeatureskyline,
wefurtherobservethatSHIFToptimallyornear-optimallyidentifiesthebestfeaturestoremove.
SHIFT critically relies on the use of properly selected SAE features. When ablating random SAE
features, we see essentially no effect on probe performance. When applying SHIFT with neurons,
essentiallynoneoftheneuronsareinterpretable,makingitdifficulttotelliftheyoughttobeablated;
seeAppendixDforexamples. Becauseofthis,weabandontheSHIFTwithneuronsbaseline. Even
using the balanced set to automatically select neurons for removal (the neuron skyline) fails to
match SHIFT’sperformance,astheneuronsmostimplicatedinspuriousfeatureclassificationare
alsousefulforground-truthclassification.
5 UNSUPERVISED CIRCUIT DISCOVERY AT SCALE
Previousworkoncircuitanalysisreliedonhuman-collecteddatasetstospecifyLMbehaviors(Wang
etal.,2023;Conmyetal.,2023;Hannaetal.,2023). However,LMsimplementnumerousinterest-
ing behaviors, many of which may be counterintuitive to humans. In this section, we adapt our
techniques to produce a near-fully-automated interpretability pipeline, starting from a large text
corpus—here, alargesubsetofThePile(Gaoetal.,2020)—andendingwiththousandsoffeature
circuitsforauto-discoveredmodelbehaviors. TheseexperimentsareperformedwithPythia-70M.
Weproceedintwosteps:
1. Behavior discovery via clustering. We interpret our large text corpus as a dataset
{(x ,y )}ofcontextsx withground-truthnexttokensy .FollowingMichaudetal.(2023),
i i i i
we associate a vector v = v(x ,y ) to each sample and apply a clustering algorithm to
i i i
{v }; this segments our large corpus into a number of smaller subcorpora corresponding
i
totheclusters. Althoughthisapproachisentirelyunsupervised,manyoftheresultingsub-
corporacapturehuman-interpretablemodelbehaviors,suchaspredictingthenextnumber
inasequence(Fig5). Weexperimentwithanumberofwaysofassigning(x ,y ) (cid:55)→ v ,
i i i
suchasusingthetraininggradient∇ logP (y |x )asinMichaudetal.(2023)aswellas
θ θ i i
approacheswhichleverageSAEactivationsorgradients. SeeApp.Gfordetails.
2. Circuitdiscovery. GivenasubcorpusD = {(x ,y )},weapplythezero-ablationvariant
i i
of our feature circuit discovery technique from §3 using the dataset D and metric m =
−logP(y |x ). Thus,toeachsubcorpusweassociateafeaturecircuit.
i i
Wepresentexampleclusters,aswellasinterestingfeaturesparticipatingintheirassociatedcircuits
(Figure 5). An interface for exploring all of our clusters and (unlabeled) circuits can be found at
feature-circuits.xyz.
While evaluating these clusters and circuits is an important open problem, we generally find that
theseclustersexposeinterestingLMbehaviors,andthattheirrespectivefeaturecircuitscanprovide
9

PublishedasaconferencepaperatICLR2025
useful insights on mechanisms of LM behavior. For instance, we automatically discover attention
featuresimplicatedinsuccessionandinduction,twophenomenathoroughlystudiedinpriorworkat
theattentionheadlevelusinghuman-curateddata(Olssonetal.,2022;Gouldetal.,2023).
Featurecircuitscanalsoshedinterestinglightontheirclusters. Forexample,whiletheclustersin
Figure 5 seem at first to each represent a single mechanism, circuit-level analysis reveals in both
casesaunionofdistinctmechanisms. Forcluster475,Pythia-70Mdetermineswhether“to[verb]”
is an appropriate object in two distinct manners (see Figure 5 caption). And for cluster 382, the
predictionofsuccessorsreliesongeneralsuccessionfeatures,aswellasmultiplenarrowinduction
featureswhichrecognizepatternslike“A3...A”.
6 RELATED WORK
Causal interpretability. Interpretability research has applied causal mediation analysis (Pearl,
2001; Robins & Greenland, 1992) to understand the mechanisms underlying particular model be-
haviorsandtheiremergence(Yuetal.,2023;Gevaetal.,2023;Hannaetal.,2023;Toddetal.,2024;
Prakash et al., 2024; Chen et al., 2024, inter alia). This typically relies on counterfactual inter-
ventions(Lewis,1973),suchasactivationpatchingorpathpatchingoncoarse-grainedcomponents
(Conmyetal.,2023;Wangetal.,2023).Sometechniquesaimto,givenahypothesizedcausalgraph,
identifyamatchingcausalmechanisminanLM(Geigeretal.,2021;2022;2023); incontrast,we
aimheretodiscovercausalmechansismswithoutstartingfromsuchhypotheses.
Robustness to spurious correlations. There is a large literature on mitigating robustness to spu-
rious correlations, including techniques which rely on directly optimizing worst-group accuracy
(Sagawaetal.,2020;Orenetal.,2019;Zhangetal.,2021;Sohonietal.,2022;Nametal.,2022),
automatically or manually reweighting data between groups (Liu et al., 2021; Nam et al., 2020;
Yaghoobzadeh et al., 2021; Utama et al., 2020; Creager et al., 2021; Idrissi et al., 2022; Orgad &
Belinkov,2023),trainingclassifierswithmorefavorableinductivebiases(Kirichenkoetal.,2023;
Zhangetal.,2022;Iskanderetal.,2024), oreditingoutundesiredconcepts(Iskanderetal.,2023;
Belrose et al., 2023; Wang et al., 2020; Ravfogel et al., 2020; 2022a;b). All of these techniques
rely on access to disambiguating labeled data in the sense of §4. Some techniques from a smaller
literaturefocusedonimageormultimodalmodelsapplywithoutsuchdata(Oikarinenetal.,2023;
Yanetal.,2023). OurmethodhereisinspiredbytheapproachofGandelsmanetal.(2024)based
oninterpretingandablatingundesiredattentionheadsinCLIP.
Feature disentanglement. In addition to recent work on SAEs for LM interpretability (Cunning-
ham et al., 2024; Bricken et al., 2023; Gao et al., 2024; Rajamanoharan et al., 2024a;b), other ap-
proachestofeaturedisentanglementincludeSchmidhuber(1992);Desjardinsetal.(2012);Kim&
Mnih(2018);Chenetal.(2016);Makhzani&Frey(2013);Heetal.(2022);Peeblesetal.(2020);
Schneider&Vlachos(2021);Burgessetal.(2017);Chenetal.(2018);Higginsetal.(2017);i.a.
7 CONCLUSION
We have introduced a method for discovering circuits on sparse features. Using this method, we
discoverhuman-interpretablecausalgraphsforasubject-verbagreementtask,aclassifier,andthou-
sandsofgeneraltokenpredictiontasks.Wecaneditthesetoffeaturesthatmodelshaveaccesstoby
ablatingsparsefeaturesthathumansdeemspurious;wefindthatthisissignificantlymoreeffective
thananeuron-basedablationmethodwhichhasanunfairadvantage.
8 LIMITATIONS
The success of our technique relies on access to SAEs for a given model. Training such SAEs
currentlyrequiresalarge(butone-time)upfrontcomputecost. Additionally,modelcomponentsnot
capturedbytheSAEswillremainuninterpretableafterapplyingourmethod.
Muchofourevaluationisqualitative. Whilewehavequantitativeevidencethatfeaturecircuitsare
usefulforimprovinggeneralizationwithoutadditionaldata(§4),evaluatingdictionariesandcircuits
withoutdownstreamtasksischallenging. Featurelabelingisalsoaqualitativeprocess;thus,labels
mayvaryacrossannotators,andmayvarydependingonthetaskofinterest.
10

PublishedasaconferencepaperatICLR2025
REPRODUCIBILITY
We release code, data and autoencoders at github.com/saprmarks/feature-circuits. Exper-
imental details can be found in appendices A, E, and G. Our experiments are conducted entirely
onopen-weightsmodels. TheGemmaScopeSAEsarepubliclyavailable(Lieberumetal.,2024).
Features for both SAE suites can be browsed on Neuronpedia (Lin & Bloom, 2023). Our clusters
andassociatedfeaturecircuitscanbebrowsedatfeature-circuits.xyz.
ACKNOWLEDGMENTS
We thank Stephen Casper, Buck Schlegeris, Ryan Greenblatt, and Neel Nanda for discussion of
ideas upstream to the experiments in §4. We thank Logan Riggs and Jannik Brinkmann for help
trainingSAEs. WealsothankJoshEngelsandMaxTegmarkfordiscussionsaboutclusteringand
sparseprojectionsrelatedto§5. S.M.issupportedbyanOpenPhilanthropyalignmentgrant. C.R.
is supported by Manifund Regrants. E.J.M. is supported by the NSF Graduate Research Fellow-
shipProgram(GrantNo.2141064). Y.B.issupportedbytheIsraelScienceFoundation(GrantNo.
448/20) and an Azrieli Foundation Early Career Faculty Fellowship. Y.B. and D.B. are supported
by a joint Open Philanthropy alignment grant. A.M. is supported by a Zuckerman postdoctoral
fellowship.
REFERENCES
Yonatan Belinkov. Probing classifiers: Promises, shortcomings, and advances. Computational
Linguistics,48(1):207–219,2022.
Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, and Stella
Biderman. LEACE: Perfect linear concept erasure in closed form. In Thirty-seventh Confer-
enceonNeuralInformationProcessingSystems,2023,LEACE:Perfectlinearconcepterasurein
closedform.
StellaBiderman,HaileySchoelkopf,QuentinGregoryAnthony,HerbieBradley,KyleO’Brien,Eric
Hallahan,MohammadAflahKhan,ShivanshuPurohit,USVSNSaiPrashanth,EdwardRaff,etal.
Pythia: Asuiteforanalyzinglargelanguagemodelsacrosstrainingandscaling. InInternational
ConferenceonMachineLearning,pp.2397–2430.PMLR,2023.
TrentonBricken, AdlyTempleton, JoshuaBatson, BrianChen, AdamJermyn, TomConerly, Nick
Turner,CemAnil,CarsonDenison,AmandaAskell,RobertLasenby,YifanWu,ShaunaKravec,
Nicholas Schiefer, Tim Maxwell, Nicholas Joseph, Zac Hatfield-Dodds, Alex Tamkin, Karina
Nguyen, Brayden McLean, Josiah E Burke, Tristan Hume, Shan Carter, Tom Henighan, and
Christopher Olah. Towards monosemanticity: Decomposing language models with dictionary
learning,TowardsMonosemanticity: DecomposingLanguageModelsWithDictionaryLearning.
TransformerCircuitsThread,2023.
ChristopherP.Burgess,IrinaHiggins,ArkaPal,LoicMatthey,NickWatters,GuillaumeDesjardins,
andAlexanderLerchner. Understandingdisentanglinginβ-VAE,2017,Understandingdisentan-
glinginβ-VAE.
Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschen-
brenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, Ilya Sutskever, and Jeff Wu.
Weak-to-strong generalization: Eliciting strong capabilities with weak supervision, Weak-to-
Strong Generalization: Eliciting Strong Capabilities With Weak Supervision. Computing Re-
searchRepository,arXiv:2312.09390,2023.
Stephen Casper, Xander Davies, Claudia Shi, Thomas Krendl Gilbert, Je´re´my Scheurer, Javier
Rando, Rachel Freedman, Tomasz Korbak, David Lindner, Pedro Freire, Tony Tong Wang,
Samuel Marks, Charbel-Raphael Segerie, Micah Carroll, Andi Peng, Phillip Christoffersen,
Mehul Damani, Stewart Slocum, Usman Anwar, Anand Siththaranjan, Max Nadeau, Eric J
Michaud, Jacob Pfau, Dmitrii Krasheninnikov, Xin Chen, Lauro Langosco, Peter Hase, Erdem
Biyik,AncaDragan,DavidKrueger,DorsaSadigh,andDylanHadfield-Menell. Openproblems
and fundamental limitations of reinforcement learning from human feedback, Open Problems
11

PublishedasaconferencepaperatICLR2025
and Fundamental Limitations of Reinforcement Learning from Human Feedback. Transactions
onMachineLearningResearch,2023. ISSN2835-8856. SurveyCertification.
AngelicaChen,RavidShwartz-Ziv,KyunghyunCho,MatthewLLeavitt,andNaomiSaphra. Sud-
dendropsintheloss: Syntaxacquisition,phasetransitions,andsimplicitybiasinMLMs. InThe
TwelfthInternationalConferenceonLearningRepresentations,2024,SuddenDropsintheLoss:
SyntaxAcquisition,PhaseTransitions,andSimplicityBiasinMLMs.
Tian Qi Chen, Xuechen Li, Roger Grosse, and David Duvenaud. Isolating sources of disentan-
glement in variational autoencoders, 2018, Isolating Sources of Disentanglement in Variational
Autoencoders.
Xi Chen, Yan Duan, Rein Houthooft, John Schulman, Ilya Sutskever, and Pieter Abbeel. In-
fogan: interpretable representation learning by information maximizing generative adversarial
nets. In Proceedings of the 30th International Conference on Neural Information Processing
Systems, NIPS’16, pp. 2180–2188, Red Hook, NY, USA, 2016. Curran Associates Inc. ISBN
9781510838819.
Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei.
Deep reinforcement learning from human preferences. Computing Research Repository,
arXiv:1706.03741,2023.
Arthur Conmy, Augustine N. Mavor-Parker, Aengus Lynch, Stefan Heimersheim, and Adria`
Garriga-Alonso. Towardsautomatedcircuitdiscoveryformechanisticinterpretability. InThirty-
seventhConferenceonNeuralInformationProcessingSystems,2023,TowardsAutomatedCircuit
DiscoveryforMechanisticInterpretability.
Elliot Creager, Joern-Henrik Jacobsen, and Richard Zemel. Environment inference for invariant
learning. In Marina Meila and Tong Zhang (eds.), Proceedings of the 38th International Con-
ference on Machine Learning, volume 139 of Proceedings of Machine Learning Research, pp.
2189–2200.PMLR,18–24Jul2021,EnvironmentInferenceforInvariantLearning.
HoagyCunningham, AidanEwart, LoganRiggs, RobertHuben, andLeeSharkey. Sparseautoen-
codersfindhighlyinterpretablefeaturesinlanguagemodels.InTheTwelfthInternationalConfer-
enceonLearningRepresentations,2024,SparseAutoencodersFindHighlyInterpretableFeatures
inLanguageModels.
MariaDe-Arteaga,AlexeyRomanov,HannaWallach,JenniferChayes,ChristianBorgs,Alexandra
Chouldechova, Sahin Geyik, Krishnaram Kenthapadi, and Adam Tauman Kalai. Bias in bios:
A case study of semantic representation bias in a high-stakes setting. In Proceedings of the
Conference on Fairness, Accountability, and Transparency, FAT* ’19, pp. 120–128, New York,
NY,USA,2019.AssociationforComputingMachinery. ISBN9781450361255,BiasinBios: A
CaseStudyofSemanticRepresentationBiasinaHigh-StakesSetting.
GuillaumeDesjardins,AaronCourville,andYoshuaBengio. Disentanglingfactorsofvariationvia
generativeentangling. ComputingResearchRepository,arXiv:1210.5474,2012.
Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna
Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, Roger Grosse,
Sam McCandlish, Jared Kaplan, Dario Amodei, Martin Wattenberg, and Christopher Olah.
Toy models of superposition. Transformer Circuits Thread, 2022. https://transformer-
circuits.pub/2022/toy model/index.html.
MatthewFinlayson,AaronMueller,SebastianGehrmann,StuartShieber,TalLinzen,andYonatan
Belinkov. Causal analysis of syntactic agreement mechanisms in neural language models. In
Chengqing Zong, Fei Xia, Wenjie Li, and Roberto Navigli (eds.), Proceedings of the 59th An-
nual Meeting of the Association for Computational Linguistics and the 11th International Joint
ConferenceonNaturalLanguageProcessing(Volume1: LongPapers),pp.1828–1843,Online,
August 2021. Association for Computational Linguistics, Causal Analysis of Syntactic Agree-
mentMechanismsinNeuralLanguageModels.
YossiGandelsman,AlexeiA.Efros,andJacobSteinhardt. InterpretingCLIP’simagerepresentation
viatext-baseddecomposition. ComputingResearchRepository,arXiv:2310.05916,2024.
12

PublishedasaconferencepaperatICLR2025
Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason
Phang, Horace He, Anish Thite, Noa Nabeshima, Shawn Presser, and Connor Leahy. The
Pile: An800GBdatasetofdiversetextforlanguagemodeling. ComputingResearchRepository,
arXiv:2101.00027,2020.
LeoGao,TomDupre´laTour,HenkTillman,GabrielGoh,RajanTroll,AlecRadford,IlyaSutskever,
Jan Leike, and Jeffrey Wu. Scaling and evaluating sparse autoencoders. Computing Research
Repository,arXiv:2406.04093,2024.
Atticus Geiger, Hanson Lu, Thomas Icard, and Christopher Potts. Causal abstractions of neural
networks. In M. Ranzato, A. Beygelzimer, Y. Dauphin, P.S. Liang, and J. Wortman Vaughan
(eds.), AdvancesinNeuralInformationProcessingSystems, volume34, pp.9574–9586.Curran
Associates,Inc.,2021,CausalAbstractionsofNeuralNetworks.
AtticusGeiger,ZhengxuanWu,HansonLu,JoshRozner,ElisaKreiss,ThomasIcard,NoahGood-
man,andChristopherPotts. Inducingcausalstructureforinterpretableneuralnetworks. InKa-
malika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato
(eds.), Proceedings of the 39th International Conference on Machine Learning, volume 162 of
Proceedings of Machine Learning Research, pp. 7324–7338. PMLR, 17–23 Jul 2022, Inducing
CausalStructureforInterpretableNeuralNetworks.
AtticusGeiger,ChrisPotts,andThomasIcard. Causalabstractionforfaithfulmodelinterpretation.
ComputingResearchRepository,arXiv:2301.04709,2023.
Mor Geva, Jasmijn Bastings, Katja Filippova, and Amir Globerson. Dissecting recall of factual
associationsinauto-regressivelanguagemodels. InHoudaBouamor,JuanPino,andKalikaBali
(eds.),Proceedingsofthe2023ConferenceonEmpiricalMethodsinNaturalLanguageProcess-
ing, pp. 12216–12235, Singapore, December 2023. Association for Computational Linguistics,
DissectingRecallofFactualAssociationsinAuto-RegressiveLanguageModels.
Rhys Gould, Euan Ong, George Ogden, and Arthur Conmy. Successor heads: Recurring, inter-
pretableattentionheadsinthewild. ComputingResearchRepository,arXiv:2312.09230,2023.
Michael Hanna, Ollie Liu, and Alexandre Variengien. How does GPT-2 compute greater-than?:
Interpreting mathematical abilities in a pre-trained language model. In Thirty-seventh Confer-
enceonNeuralInformationProcessingSystems,2023,HowdoesGPT-2computegreater-than?:
Interpretingmathematicalabilitiesinapre-trainedlanguagemodel.
MichaelHanna,SandroPezzelle,andYonatanBelinkov. Havefaithinfaithfulness: Goingbeyond
circuit overlap when finding model mechanisms. In ICML 2024 Workshop on Mechanistic In-
terpretability, 2024, Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding
ModelMechanisms.
PeterHase,MohitBansal,PeterClark,andSarahWiegreffe.Theunreasonableeffectivenessofeasy
trainingdataforhardtasks. InLun-WeiKu,AndreMartins,andVivekSrikumar(eds.),Proceed-
ings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1:
LongPapers),pp.7002–7024,Bangkok,Thailand,August2024.AssociationforComputational
Linguistics,TheUnreasonableEffectivenessofEasyTrainingDataforHardTasks.
T. He, Z. Li, Y. Gong, Y. Yao, X. Nie, and Y. Yin. Exploring linear feature disentanglement for
neuralnetworks. In2022IEEEInternationalConferenceonMultimediaandExpo(ICME),pp.
1–6,LosAlamitos,CA,USA,jul2022.IEEEComputerSociety,ExploringLinearFeatureDis-
entanglementforNeuralNetworks.
Irina Higgins, Loic Matthey, Arka Pal, Christopher Burgess, Xavier Glorot, Matthew Botvinick,
Shakir Mohamed, and Alexander Lerchner. beta-VAE: Learning basic visual concepts with a
constrained variational framework. In International Conference on Learning Representations,
2017,beta-VAE:LearningBasicVisualConceptswithaConstrainedVariationalFramework.
Badr Youbi Idrissi, Martin Arjovsky, Mohammad Pezeshki, and David Lopez-Paz. Simple data
balancing achieves competitive worst-group-accuracy. In Bernhard Scho¨lkopf, Caroline Uhler,
andKunZhang(eds.),ProceedingsoftheFirstConferenceonCausalLearningandReasoning,
volume 177 of Proceedings of Machine Learning Research, pp. 336–351. PMLR, 11–13 Apr
2022,Simpledatabalancingachievescompetitiveworst-group-accuracy.
13

PublishedasaconferencepaperatICLR2025
ShadiIskander,KiraRadinsky,andYonatanBelinkov.Shieldedrepresentations:Protectingsensitive
attributesthroughiterativegradient-basedprojection. InAnnaRogers,JordanBoyd-Graber,and
Naoaki Okazaki (eds.), Findings of the Association for Computational Linguistics: ACL 2023,
pp.5961–5977,Toronto,Canada,July2023.AssociationforComputationalLinguistics,Shielded
Representations: ProtectingSensitiveAttributesThroughIterativeGradient-BasedProjection.
Shadi Iskander, Kira Radinsky, and Yonatan Belinkov. Leveraging prototypical representations
for mitigating social bias without demographic information. Computing Research Repository,
2403.09516,2024.
Been Kim, Martin Wattenberg, Justin Gilmer, Carrie Cai, James Wexler, Fernanda Viegas, et al.
Interpretability beyond feature attribution: Quantitative testing with concept activation vectors
(TCAV). InProceedingsofthe35thInternationalConferenceonMachineLearning,pp.2668–
2677.PMLR,2018.
HyunjikKimandAndriyMnih. Disentanglingbyfactorising. InJenniferDyandAndreasKrause
(eds.),Proceedingsofthe35thInternationalConferenceonMachineLearning,volume80ofPro-
ceedingsofMachineLearningResearch,pp.2649–2658.PMLR,10–15Jul2018,Disentangling
byFactorising.
DiederikP.KingmaandJimmyBa. Adam:Amethodforstochasticoptimization,Adam:AMethod
forStochasticOptimization. CoRR,abs/1412.6980,2014.
Polina Kirichenko, Pavel Izmailov, and Andrew Gordon Wilson. Last layer re-training is suffi-
cientforrobustnesstospuriouscorrelations.ComputingResearchRepository,arXiv:2204.02937,
2023.
Ja´nosKrama´r,TomLieberum,RohinShah,andNeelNanda.AtP*:Anefficientandscalablemethod
forlocalizingllmbehaviourtocomponents. ComputingResearchRepository,arXiv:2403.00745,
2024.
DavidK.Lewis. Counterfactuals. Blackwell,Malden,Mass.,1973.
TomLieberum,SenthooranRajamanoharan,ArthurConmy,LewisSmith,NicolasSonnerat,Vikrant
Varma,Ja´nosKrama´r,AncaDragan,RohinShah,andNeelNanda. Gemmascope: Opensparse
autoencoderseverywhereallatonceongemma2,2024.
JohnnyLinandJosephBloom. Neuronpedia: Interactivereferenceandtoolingforanalyzingneural
networks,2023,Neuronpedia:InteractiveReferenceandToolingforAnalyzingNeuralNetworks.
Softwareavailablefromneuronpedia.org.
Evan Z Liu, Behzad Haghgoo, Annie S Chen, Aditi Raghunathan, Pang Wei Koh, Shiori Sagawa,
Percy Liang, and Chelsea Finn. Just train twice: Improving group robustness without training
groupinformation.InMarinaMeilaandTongZhang(eds.),Proceedingsofthe38thInternational
Conference on Machine Learning, volume 139 of Proceedings of Machine Learning Research,
pp.6781–6792.PMLR,18–24Jul2021,JustTrainTwice: ImprovingGroupRobustnesswithout
TrainingGroupInformation.
IlyaLoshchilovandFrankHutter. Decoupledweightdecayregularization. InInternationalConfer-
enceonLearningRepresentations,2017,DecoupledWeightDecayRegularization.
AlirezaMakhzaniandBrendanJ.Frey. k-sparseautoencoders,k-SparseAutoencoders. Computing
ResearchRepository,abs/1312.5663,2013.
KevinMeng,DavidBau,AlexAndonian,andYonatanBelinkov.Locatingandeditingfactualassoci-
ationsinGPT.AdvancesinNeuralInformationProcessingSystems,36,2022.arXiv:2202.05262.
Eric J Michaud, Ziming Liu, Uzay Girit, and Max Tegmark. The quantization model of neural
scaling. In Thirty-seventh Conference on Neural Information Processing Systems, 2023, The
QuantizationModelofNeuralScaling.
14

PublishedasaconferencepaperatICLR2025
Aaron Mueller, Jannik Brinkmann, Millicent Li, Samuel Marks, Koyena Pal, Nikhil Prakash, Can
Rager, Aruna Sankaranarayanan, Arnab Sen Sharma, Jiuding Sun, Eric Todd, David Bau, and
Yonatan Belinkov. The quest for the right mediator: A history, survey, and theoretical ground-
ing of causal interpretability, 2024, The Quest for the Right Mediator: A History, Survey, and
TheoreticalGroundingofCausalInterpretability.
Junhyun Nam, Hyuntak Cha, Sungsoo Ahn, Jaeho Lee, and Jinwoo Shin. Learning from failure:
Trainingdebiasedclassifierfrombiasedclassifier. InProceedingsofthe34thInternationalCon-
ferenceonNeuralInformationProcessingSystems,NIPS’20,RedHook,NY,USA,2020.Curran
AssociatesInc. ISBN9781713829546.
JunhyunNam, JaehyungKim, JaehoLee, andJinwooShin. Spreadspuriousattribute: Improving
worst-groupaccuracywithspuriousattributeestimation,2022.
NeelNanda. Attributionpatching: Activationpatchingatindustrialscale,2022,AttributionPatch-
ing: ActivationPatchingAtIndustrialScale.
NeelNanda.Opensourcereplication&commentaryonAnthropic’sdictionarylearningpaper,2023,
OpenSourceReplication&CommentaryonAnthropic’sDictionaryLearningPaper.
NeelNanda,SenthooranRajamanoharan,Ja´nosKrama´r,andRohinShah. Factfinding: Attempting
toreverse-engineerfactualrecallontheneuronlevel,2023,FactFinding:AttemptingtoReverse-
EngineerFactualRecallontheNeuronLevel.
RichardNgo,LawrenceChan,andSo¨renMindermann.Thealignmentproblemfromadeeplearning
perspective. ComputingResearchRepository,arXiv:2209.00626,2024.
Tuomas Oikarinen, Subhro Das, Lam M. Nguyen, and Tsui-Wei Weng. Label-free concept bot-
tleneck models. In The Eleventh International Conference on Learning Representations, 2023,
Label-freeConceptBottleneckModels.
CatherineOlsson, NelsonElhage, NeelNanda, NicholasJoseph, NovaDasSarma, TomHenighan,
BenMann,AmandaAskell,YuntaoBai,AnnaChen,TomConerly,DawnDrain,DeepGanguli,
Zac Hatfield-Dodds, Danny Hernandez, Scott Johnston, Andy Jones, Jackson Kernion, Liane
Lovitt,KamalNdousse,DarioAmodei,TomBrown,JackClark,JaredKaplan,SamMcCandlish,
and Chris Olah. In-context learning and induction heads. Transformer Circuits Thread, 2022.
https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html.
YonatanOren,ShioriSagawa,TatsunoriB.Hashimoto,andPercyLiang.Distributionallyrobustlan-
guagemodeling. InKentaroInui,JingJiang,VincentNg,andXiaojunWan(eds.),Proceedings
ofthe2019ConferenceonEmpiricalMethodsinNaturalLanguageProcessingandthe9thInter-
nationalJointConferenceonNaturalLanguageProcessing(EMNLP-IJCNLP),pp.4227–4237,
HongKong,China,November2019.AssociationforComputationalLinguistics,Distributionally
RobustLanguageModeling.
HadasOrgadandYonatanBelinkov. BLIND:Biasremovalwithnodemographics. InAnnaRogers,
JordanBoyd-Graber,andNaoakiOkazaki(eds.),Proceedingsofthe61stAnnualMeetingofthe
Association for Computational Linguistics (Volume 1: Long Papers), pp. 8801–8821, Toronto,
Canada,July2023.AssociationforComputationalLinguistics,BLIND:BiasRemovalWithNo
Demographics.
JudeaPearl. Directandindirecteffects. InProceedingsoftheSeventeenthConferenceonUncer-
tainty in Artificial Intelligence, UAI’01, pp. 411–420, San Francisco, CA, USA, 2001. Morgan
KaufmannPublishersInc. ISBN1558608001.
F.Pedregosa,G.Varoquaux,A.Gramfort,V.Michel,B.Thirion,O.Grisel,M.Blondel,P.Pretten-
hofer,R.Weiss,V.Dubourg,J.Vanderplas,A.Passos,D.Cournapeau,M.Brucher,M.Perrot,and
E.Duchesnay. Scikit-learn:MachinelearninginPython. JournalofMachineLearningResearch,
12:2825–2830,2011.
WilliamPeebles,JohnPeebles,Jun-YanZhu,AlexeiA.Efros,andAntonioTorralba. Thehessian
penalty:Aweakpriorforunsuperviseddisentanglement.InProceedingsofEuropeanConference
onComputerVision(ECCV),2020.
15

PublishedasaconferencepaperatICLR2025
Nikhil Prakash, Tamar Rott Shaham, Tal Haklay, Yonatan Belinkov, and David Bau. Fine-tuning
enhances existing mechanisms: A case study on entity tracking. In Proceedings of the 2024
InternationalConferenceonLearningRepresentations,2024. arXiv:2402.14811.
Senthooran Rajamanoharan, Arthur Conmy, Lewis Smith, Tom Lieberum, Vikrant Varma, Ja´nos
Krama´r,RohinShah,andNeelNanda. Improvingdictionarylearningwithgatedsparseautoen-
coders. ComputingResearchRepository,arXiv:2404.16014,2024a.
SenthooranRajamanoharan,TomLieberum,NicolasSonnerat,ArthurConmy,VikrantVarma,Ja´nos
Krama´r,andNeelNanda.Jumpingahead:Improvingreconstructionfidelitywithjumprelusparse
autoencoders, Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Au-
toencoders. ComputingResearchRepository,arXiv:2407.14435,2024b.
ShauliRavfogel,YanaiElazar,HilaGonen,MichaelTwiton,andYoavGoldberg.Nullitout:Guard-
ing protected attributes by iterative nullspace projection. In Dan Jurafsky, Joyce Chai, Natalie
Schluter, and Joel Tetreault (eds.), Proceedings of the 58th Annual Meeting of the Association
forComputationalLinguistics,pp.7237–7256,Online,July2020.AssociationforComputational
Linguistics,NullItOut: GuardingProtectedAttributesbyIterativeNullspaceProjection.
ShauliRavfogel,MichaelTwiton,YoavGoldberg,andRyanDCotterell. Linearadversarialconcept
erasure. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and
Sivan Sabato (eds.), Proceedings of the 39th International Conference on Machine Learning,
volume162ofProceedingsofMachineLearningResearch,pp.18400–18421.PMLR,17–23Jul
2022a,LinearAdversarialConceptErasure.
ShauliRavfogel,FranciscoVargas,YoavGoldberg,andRyanCotterell.Adversarialconcepterasure
in kernel space. In Yoav Goldberg, Zornitsa Kozareva, and Yue Zhang (eds.), Proceedings of
the 2022 Conference on Empirical Methods in Natural Language Processing, pp. 6034–6055,
AbuDhabi,UnitedArabEmirates,December2022b.AssociationforComputationalLinguistics,
AdversarialConceptErasureinKernelSpace.
JamesM.RobinsandSanderGreenland. Identifiabilityandexchangeabilityfordirectandindirect
effects, Identifiability and Exchangeability for Direct and Indirect Effects. Epidemiology, 3(2):
143–155,1992. ISSN10443983.
Shiori Sagawa, Pang Wei Koh, Tatsunori B. Hashimoto, and Percy Liang. Distributionally robust
neuralnetworks. InInternationalConferenceonLearningRepresentations, 2020, Distribution-
allyRobustNeuralNetworks.
Ju¨rgenSchmidhuber. LearningFactorialCodesbyPredictabilityMinimization,LearningFactorial
CodesbyPredictabilityMinimization. NeuralComputation,4(6):863–879,111992. ISSN0899-
7667.
Johannes Schneider and Michalis Vlachos. Explaining neural networks by decoding layer activa-
tions. InAdvancesinIntelligentDataAnalysisXIX:19thInternationalSymposiumonIntelligent
Data Analysis, IDA 2021, Porto, Portugal, April 26–28, 2021, Proceedings, pp. 63–75, Berlin,
Heidelberg, 2021. Springer-Verlag. ISBN 978-3-030-74250-8, Explaining Neural Networks by
DecodingLayerActivations.
NimitSharadSohoni,MaziarSanjabi,NicolasBallas,AdityaGrover,ShaoliangNie,HamedFirooz,
andChristopherRe. BARACK:Partiallysupervisedgrouprobustnesswithguarantees. InICML
2022: Workshop on Spurious Correlations, Invariance and Stability, 2022, BARACK: Partially
SupervisedGroupRobustnessWithGuarantees.
Mukund Sundararajan, Ankur Taly, and Qiqi Yan. Axiomatic attribution for deep networks. In
Proceedingsofthe34thInternationalConferenceonMachineLearning-Volume70,ICML’17,
pp.3319–3328.JMLR.org,2017.
Aaquib Syed, Can Rager, and Arthur Conmy. Attribution patching outperforms automated cir-
cuitdiscovery. InNeurIPSWorkshoponAttributingModelBehavioratScale,2023,Attribution
PatchingOutperformsAutomatedCircuitDiscovery.
16

PublishedasaconferencepaperatICLR2025
GemmaTeam,MorganeRiviere,ShreyaPathak,PierGiuseppeSessa,CassidyHardin,SuryaBhu-
patiraju, Le´onard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Rame´, Johan Fer-
ret, Peter Liu, Pouya Tafti, Abe Friesen, Michelle Casbon, Sabela Ramos, Ravin Kumar, Char-
line Le Lan, Sammy Jerome, Anton Tsitsulin, Nino Vieillard, Piotr Stanczyk, Sertan Girgin,
Nikola Momchev, Matt Hoffman, Shantanu Thakoor, Jean-Bastien Grill, Behnam Neyshabur,
Olivier Bachem, Alanna Walton, Aliaksei Severyn, Alicia Parrish, Aliya Ahmad, Allen Hutchi-
son, Alvin Abdagic, Amanda Carl, Amy Shen, Andy Brock, Andy Coenen, Anthony Laforge,
AntoniaPaterson,BenBastian,BilalPiot,BoWu,BrandonRoyal,CharlieChen,ChintuKumar,
Chris Perry, Chris Welty, Christopher A. Choquette-Choo, Danila Sinopalnikov, David Wein-
berger,DimpleVijaykumar,DominikaRogozin´ska,DustinHerbison,ElisaBandy,EmmaWang,
Eric Noland, Erica Moreira, Evan Senter, Evgenii Eltyshev, Francesco Visin, Gabriel Rasskin,
Gary Wei, Glenn Cameron, Gus Martins, Hadi Hashemi, Hanna Klimczak-Plucin´ska, Harleen
Batra,HarshDhand,IvanNardini,JacindaMein,JackZhou,JamesSvensson,JeffStanway,Jetha
Chan,JinPengZhou,JoanaCarrasqueira,JoanaIljazi,JocelynBecker,JoeFernandez,Joostvan
Amersfoort, Josh Gordon, Josh Lipschultz, Josh Newlan, Ju yeong Ji, Kareem Mohamed, Kar-
tikeya Badola, Kat Black, Katie Millican, Keelin McDonell, Kelvin Nguyen, Kiranbir Sodhia,
KishGreene,LarsLoweSjoesund,LaurenUsui,LaurentSifre,LenaHeuermann,LeticiaLago,
LillyMcNealus,LivioBaldiniSoares,LoganKilpatrick,LucasDixon,LucianoMartins,Machel
Reid,ManvinderSingh,MarkIverson,MartinGo¨rner,MatVelloso,MateoWirth,MattDavidow,
Matt Miller, Matthew Rahtz, Matthew Watson, Meg Risdal, Mehran Kazemi, Michael Moyni-
han, Ming Zhang, Minsuk Kahng, Minwoo Park, Mofi Rahman, Mohit Khatwani, Natalie Dao,
NenshadBardoliwalla,NeshDevanathan,NetaDumai,NilayChauhan,OscarWahltinez,Pankil
Botarda, Parker Barnes, Paul Barham, Paul Michel, Pengchong Jin, Petko Georgiev, Phil Culli-
ton,PradeepKuppala,RamonaComanescu,RamonaMerhej,ReenaJana,RezaArdeshirRokni,
RishabhAgarwal,RyanMullins,SamanehSaadat,SaraMcCarthy,SarahPerrin,Se´bastienM.R.
Arnold,SebastianKrause,ShengyangDai,ShrutiGarg,ShrutiSheth,SueRonstrom,SusanChan,
TimothyJordan,TingYu,TomEccles,TomHennigan,TomasKocisky,TulseeDoshi,VihanJain,
VikasYadav, VilobhMeshram, VishalDharmadhikari, WarrenBarkley, WeiWei, WenmingYe,
WoohyunHan,WoosukKwon,XiangXu,ZheShen,ZhitaoGong,ZichuanWei,VictorCotruta,
PhoebeKirk,AnandRao,MinhGiang,LudovicPeran,TrisWarkentin,EliCollins,JoelleBarral,
ZoubinGhahramani, RaiaHadsell, D.Sculley, JeanineBanks, AncaDragan, SlavPetrov, Oriol
Vinyals,JeffDean,DemisHassabis,KorayKavukcuoglu,ClementFarabet,ElenaBuchatskaya,
SebastianBorgeaud,NoahFiedel,ArmandJoulin,KathleenKenealy,RobertDadashi,andAlek
Andreev. Gemma2: Improvingopenlanguagemodelsatapracticalsize,2024.
AdlyTempleton,TomConerly,JonathanMarcus,JackLindsey,TrentonBricken,BrianChen,Adam
Pearce, CraigCitro, EmmanuelAmeisen, AndyJones, HoagyCunningham, NicholasLTurner,
CallumMcDougall,MonteMacDiarmid,C.DanielFreeman,TheodoreR.Sumers,EdwardRees,
JoshuaBatson,AdamJermyn,ShanCarter,ChrisOlah,andTomHenighan.Scalingmonoseman-
ticity: Extractinginterpretablefeaturesfromclaude3sonnet,ScalingMonosemanticity: Extract-
ingInterpretableFeaturesfromClaude3Sonnet. TransformerCircuitsThread,2024.
EricTodd,MillicentL.Li,ArnabSenSharma,AaronMueller,ByronC.Wallace,andDavidBau.
Functionvectorsinlargelanguagemodels. InProceedingsofthe2024InternationalConference
onLearningRepresentations,2024.
PrasetyaAjieUtama,NafiseSadatMoosavi,andIrynaGurevych. TowardsdebiasingNLUmodels
fromunknownbiases. InBonnieWebber,TrevorCohn,YulanHe,andYangLiu(eds.),Proceed-
ingsof the2020 ConferenceonEmpirical MethodsinNatural LanguageProcessing (EMNLP),
pp. 7597–7610, Online, November 2020. Association for Computational Linguistics, Towards
DebiasingNLUModelsfromUnknownBiases.
Jesse Vig, Sebastian Gehrmann, Yonatan Belinkov, Sharon Qian, Daniel Nevo, Yaron Singer, and
Stuart Shieber. Investigating gender bias in language models using causal mediation analysis.
In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), Advances in Neural
Information Processing Systems, volume 33, pp. 12388–12401. Curran Associates, Inc., 2020,
InvestigatingGenderBiasinLanguageModelsUsingCausalMediationAnalysis.
KevinRoWang,AlexandreVariengien,ArthurConmy,BuckShlegeris,andJacobSteinhardt.Inter-
pretabilityinthewild: acircuitforindirectobjectidentificationinGPT-2small. InTheEleventh
17

PublishedasaconferencepaperatICLR2025
InternationalConferenceonLearningRepresentations,2023,InterpretabilityintheWild: aCir-
cuitforIndirectObjectIdentificationinGPT-2Small.
TianluWang,XiVictoriaLin,NazneenFatemaRajani,BryanMcCann,VicenteOrdonez,andCaim-
ingXiong. Double-harddebias: Tailoringwordembeddingsforgenderbiasmitigation. InDan
Jurafsky,JoyceChai,NatalieSchluter,andJoelTetreault(eds.),Proceedingsofthe58thAnnual
MeetingoftheAssociationforComputationalLinguistics,pp.5443–5453,Online,July2020.As-
sociation for Computational Linguistics, Double-Hard Debias: Tailoring Word Embeddings for
GenderBiasMitigation.
Yadollah Yaghoobzadeh, Soroush Mehri, Remi Tachet des Combes, T. J. Hazen, and Alessandro
Sordoni. Increasing robustness to spurious correlations using forgettable examples. In Paola
Merlo, Jorg Tiedemann, and Reut Tsarfaty (eds.), Proceedings of the 16th Conference of the
European Chapter of the Association for Computational Linguistics: Main Volume, pp. 3319–
3332, Online, April 2021. Association for Computational Linguistics, Increasing Robustness to
SpuriousCorrelationsusingForgettableExamples.
An Yan, Yu Wang, Yiwu Zhong, Zexue He, Petros Karypis, Zihan Wang, Chengyu Dong, Amil-
care Gentili, Chun-Nan Hsu, Jingbo Shang, and Julian McAuley. Robust and interpretable
medical image classifiers via concept bottleneck models. Computing Research Repository,
arXiv:2310.03182,2023.
Qinan Yu, Jack Merullo, and Ellie Pavlick. Characterizing mechanisms for factual recall in lan-
guage models. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), Proceedings of the 2023
ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,pp.9924–9959,Singapore,
December2023.AssociationforComputationalLinguistics,CharacterizingMechanismsforFac-
tualRecallinLanguageModels.
JohnR.Zech,MarcusA.Badgeley,ManwayLiu,AnthonyB.Costa,JosephJ.Titano,andEricKarl
Oermann. Variablegeneralizationperformanceofadeeplearningmodeltodetectpneumoniain
chestradiographs: Across-sectionalstudy,Variablegeneralizationperformanceofadeeplearn-
ing model to detect pneumonia in chest radiographs: A cross-sectional study. PLOS Medicine,
15(11):e1002683,November2018. ISSN1549-1676.
Jingzhao Zhang, Aditya Krishna Menon, Andreas Veit, Srinadh Bhojanapalli, Sanjiv Kumar, and
SuvritSra. Copingwithlabelshiftviadistributionallyrobustoptimisation. InInternationalCon-
ferenceonLearningRepresentations,2021,CopingwithLabelShiftviaDistributionallyRobust
Optimisation.
MichaelZhang,NimitSSohoni,HongyangRZhang,ChelseaFinn,andChristopherRe.Correct-N-
Contrast: Acontrastiveapproachforimprovingrobustnesstospuriouscorrelations. InKamalika
Chaudhuri,StefanieJegelka,LeSong,CsabaSzepesvari,GangNiu,andSivanSabato(eds.),Pro-
ceedingsofthe39thInternationalConferenceonMachineLearning,volume162ofProceedings
ofMachineLearningResearch, pp.26484–26516.PMLR,17–23Jul2022, Correct-N-Contrast:
AContrastiveApproachforImprovingRobustnesstoSpuriousCorrelations.
Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan,
Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, et al. Representation engineering:
A top-down approach to AI transparency. Computing Research Repository, arXiv:2310.01405,
2023.
A METHODOLOGICAL DETAILS FOR FEATURE CIRCUIT DISCOVERY
A.1 COMPUTINGEDGEWEIGHTS
Let e be an edge between an upstream node u and downstream node d; let also M be the set of
nodesmintermediatebetweenuandd. Wedefinetheweightoftheedgeetobetheeffectonthe
metricmwheninterveningtoset
d=d(x |do(u=u ,m=m :m∈M)).
clean patch clean
18

PublishedasaconferencepaperatICLR2025
Templatic data: No position aggregation Non-templatic data: Sum aggregation
sum
0, a1 1, a1 1, b1 0, a1 1, a1 1, b1 a1 b1
The doctor It’s strange …
sum
0, a1 1, a1 1, b1 0, a1 1, a1 1, b1 a1 b1
The children Doctor Johnson …
mean
mean
0, a1 1, a1 1, b1
a1 b1
Figure 6: Aggregation of node/edge effects across examples (and sometimes, across token posi-
tions). Each feature is labeled as “token position, feature index.” If we have templatic data, we
preservetokenpositioninformation,andtreatthesamefeaturesindifferenttokenpositionsasdif-
ferentfeatures. Ifwehavemoregeneralnon-templaticdata,wefirstsumacrosspositions,andthen
taketheexample-wisemeanoftheposition-aggregatedeffects.
Intuitively,thiscapturestheindirecteffectofuonmviathedirecteffectond,butexcludingeffects
ondmediatedbysomeotherintermediatenodem.
Aswithnodes,weemployalinearapproximation:
IˆE(m;e;x clean ,x patch )= ∇ d m| dclean ∇ u,stop(M) d (cid:12) (cid:12) uclean (u patch −u clean ) (5)
where∇ ddenotesthegradientofdwithrespecttouwhentreatingallm∈Masconstant.
u,stop(M)
Inpractice,thisiscomputedbyapplyingstop-gradientstoallintermediatenodesmduringpytorch’s
backwardspass.
IfdisanSAEerror,thenthenaiveapproachtocomputingisexpressioninvolvesperformingd
model
backwards passes; fortunately we can still compute the product in a single backwards pass as ex-
plainedin§A.3.
A.2 AGGREGATINGACROSSTOKENPOSITIONSANDEXAMPLES
Figure6summarizeshowweaggregateeffectsacrossexamples(andoptionallyacrosstokenposi-
tions). Fortemplaticdatawheretokensinmatchingpositionsplayconsistentroles(see§3.2,3.3),
wetakethemeaneffectofnodes/edgesacrossexamples. Inthiscase,wetreatthesamefeature(or
neuron)indifferenttokenpositionsasdifferentnodesaltogetherinthecircuit,eachwiththeirown
separateeffectsontargetmetricm.
Fornon-templaticdata(§4,5),wefirstsumtheeffectsofcorrespondingnodes/edgesacrosstoken
positionsbeforetakingtheexample-wisemean. Thismeansthateachfeatureappearsinthecircuit
once,representingitseffectsatalltokenpositionsinaninput.
A.3 PRACTICALCONSIDERATIONS
Herewereviewanumberoftricksthatweusetocomputethequantitiesdefinedaboveefficiently.
Thebackboneofourapproachisto, givenanactivationx ∈ Rdmodel ofsomesubmoduleforwhich
wehaveanSAE,usetheSAEtocomputethequantitiesf (x)andϵ(x)in(1),andthenintervenein
i
ourmodel’sforwardpasstoset
(cid:88)
x← f (x)v +b+ϵ(x). (6)
i i
i
Even though x was already numerically equal to the right-hand side of (6), after the intervention
thecomputationgraphwillincorporatethevariablesf (x)andϵ(x). Thus,whenweusePytorch’s
i
autograd algorithm to peform backpropogation of downstream quantities, we will automatically
computegradientsforthesevariables.
19

PublishedasaconferencepaperatICLR2025
Analternativeapproachforcomputinggradients(whichwedonotuse)istosimplyrunthemodel
withoutinterventions,usebackpropogationtocomputeallgradients∇ m,andusetheformulas
x
∇ m=∇ m·v , ∇ m=∇ m
fi x i ϵ x
whichfollowfromthechainrulewhenmisanyfunctionofx.
StopgradientsonSAEerrorstocomputeSAEfeaturegradients. Thenaturalwaytocompute
theSAEerrorϵ(x)isbyfirstusingtheSAEtocomputexˆandthensettingϵ(x)=x−xˆ. However,
ifwetakethisapproach,thenafterapplyingtheintervention(6)wewouldhave
∇ m=∇ m∇ xd =∇ m∇ (xˆ+xu−xˆ)=0
fi vxd fi xd fi
wherexd isthecopyofxdownstreamoff inthecomputationgraph,andxu isthecopyupstream
i
off . Tofixthis,weapplyastopgradienttoϵ(x)sothatxd =xˆ+stopgrad(xu−xˆ).
i
Pass-throughgradients. Althoughthestopgradientfromabovesolvestheproblemofvanishing
gradients for the f , it interferes with the backpropogation of gradients to further upstream nodes.
i
Inordertorestoreexactgradientcomputation,weimplementapass-throughgradientonthecom-
putationofourdictionary. Thatis,inthenotationabove,weinterveneinthebackwardspassofour
modeltoset
∇ m←∇ m.
xu xd
Jacobian-vectorproducts. Donenaively,computingthequantityin(5)whendisanSAEerrors
wouldtakeO(d )backwardspasses. Fortunately,onecanusethefollowingtrick: whenAisa
model
constant1×nmatrix,x∈Rm,andy=y(x)∈Rnisafunctionofx,wehave
A∇ y=∇ (Ay)
x x
wheretheright-handsideisa1×mJacobianwhichcanbecomputedwithasinglebackwardpass.
Thuswecancompute(5)withonlytwobackwardspassesbyfirstcomputing ∇ m| andthen
(cid:0) (cid:1)
d dclean
computing∇ ∇ m| withanotherbackwardspass,wherethesecond ∇ m| istreatedas
u d dclean d dclean
aconstant(e.g.,bydetachingitinPytorch).
B DETAILS ON SPARSE AUTOENCODERS
B.1 PYTHIA-70MSPARSEAUTOENCODERS
B.1.1 ARCHITECTURE
Following Bricken et al. (2023), our SAEs for Pythia-70M are one-layer MLPs with a tied pre-
encoderbias. Inmoredetail,ourSAEshaveparameters
W
E
∈RdSAE×dmodel,W
D
∈Rdmodel×dSAE, b
E
∈RdSAE,b
D
∈Rdmodel
wherethecolumnsofW
D
areconstrainedtobeunitvectors. Givenaninputactivationx ∈ Rdmodel,
wecomputethesparsefeaturesactivationsvia
f =[f (x) ... f (x)]=ReLU(W (x−b )+b )
1 dSAE E D E
withtheReLUnonlinearityappliedcoordinatewiseandreconstructionsvia
xˆ =W f +b .
D D
Thefeaturevectorsv
i
∈Rdmodel arethecolumnsofW
D
.
B.1.2 TRAINING
Fix a specific choice of activation in Pythia-70M, e.g. MLP output, attention output, or residual
streaminaparticularlayer. FollowingCunninghametal.(2024);Brickenetal.(2023)wetrainan
SAEforthisactivationbysamplingrandomtextfromThePile(Gaoetal.,2020)(specificallythe
20

PublishedasaconferencepaperatICLR2025
first128tokensofrandomdocuments),extractingthevaluesxforthisactivationovereverytoken,
andthentrainingourSAEtominimizealossfunction
L=L +λL =∥xˆ−x∥ +λ∥f∥
reconstruction sparsity 2 1
consistingofaL2reconstructionlossandaL1regularizationtermtopromotesparsity. Thislossis
optimizedusingavariantofAdam(Kingma&Ba,2014)adaptedtoensurethatthecolumnsofW
D
areunitvectors(seeBrickenetal.(2023)orourcodefordetails). Weuseλ = 0.1andalearning
rateof10−4.
FollowingNanda(2023),wecacheactivationsfrom10000contextsinabufferandrandomlysample
batchesofsize214fortrainingourSAE.Whenthebufferishalf-depleted,wereplenishitwithfresh
tokens from The Pile. We train for 120000 steps, resulting in a total of about 2 billion training
tokens.
AmajorobstacleintrainingSAEsisdeadfeatures,thatis,neuronsinthemiddlelayeroftheSAE
which never or rarely activate. We mitigate this by, every 25000 training steps, reinitializing fea-
tureswhichhavenotactivatedintheprevious12500stepsusingthesamereinitializationprocedure
describedinBrickenetal.(2023).
Finally, we use a linear learning rate warmup of 1000 steps at the start of training and after every
timethatneuronsareresampled.
B.1.3 EVALUATION
Herewereportonvariouseasy-to-quantifymetricsofSAEquality.Notethatthesemetricsleaveout
importantqualitativepropertiesoftheseSAEs,suchastheinterpretabilityoftheirfeatures(App.F).
Ourmetricsare:
• Varianceexplained,asmeasuredby1− Var(x−xˆ).
Var(x)
• AverageL1,andL0normsoff.
• Percentage of features alive as measured by features which activate at least once on a
batchof512tokens.
• Cross entropy (CE) difference and percentage of CE recovered. The CE difference is
the difference between the model’s original CE loss and the model’s CE loss when inter-
veningtosetxtothereconstructionxˆ. WeobtainpercentageofCErecoveredbydividing
thisdifferencebythedifferencebetweentheoriginalCElossandtheCElosswhenzero-
ablatingx. TheseCElossesarecomputedaveragedoverabatchof128contextsoflength
128.
These metrics are shown in Tables 3–6. Note that we index residual stream activations to be the
layer which outputs the activation (so the layer 0 residual stream is not the embeddings, and the
layer5residualstreamistheoutputofthefinallayer,immediatelyprecedingthefinaldecoder).
%VarianceExplained L1 L0 %Alive CEDiff %CERecovered
96 1 3 36 0.17 98
Table3: EmbeddingSAEevaluation.
B.2 GEMMA-2-2BSPARSEAUTOENCODERS
For Gemma-2-2B, we use the Gemma Scope SAEs released by Lieberum et al. (2024), which are
basedontheJump-ReLUarchitectureproposedbyRajamanoharanetal.(2024b). WeusetheSAEs
of width 16384. There exist SAEs for the attention, MLP, and residual vectors for each of the 26
layersinthemodel. However,theattentionandMLPSAEsaretrainedatdifferentpositionsthanin
Pythia: attentionSAEsaretrainedontheinputtotheoutprojection,andMLPSAEsaretrainedon
theoutputoftheLayerNormfollowingtheMLP.TheembeddingSAEsareexperimentalandhave
adictionarysizeofonly4000,sowedonotusetheminourexperiments.
21

PublishedasaconferencepaperatICLR2025
Layer %VarianceExplained L1 L0 %Alive CEDiff %CERecovered
Attn0 92% 8 128 17% 0.02 99%
Attn1 87% 9 127 17% 0.03 94%
Attn2 90% 19 215 12% 0.05 93%
Attn3 89% 12 169 13% 0.03 93%
Attn4 83% 8 132 14% 0.01 95%
Attn5 89% 11 144 20% 0.02 93%
Table4: AttentionSAEevaluationbylayer.
Layer %VarianceExplained L1 L0 %Alive CEDiff %CERecovered
MLP0 97% 5 5 40% 0.10 99%
MLP1 85% 8 69 44% 0.06 95%
MLP2 99% 12 88 31% 0.11 88%
MLP3 88% 20 160 25% 0.12 94%
MLP4 92% 20 100 29% 0.14 90%
MLP5 96% 31 102 35% 0.15 97%
Table5: MLPSAEevaluationbylayer.
There exist multiple SAEs for every submodule. The primary difference between them is their
averageL0norm.3 Neuronpedia(Lin&Bloom,2023)usestheSAEswiththeL0normclosestto
100;wedothesame.
OneoftheprimarytechnicalchallengesinusingtheGemmaScopeSAEsistheexistenceofBOS
features. ThesearefeaturesthatareactiveprimarilyoronlyonBOStokens, andwhosetoplogits
are generally not informative. These features are difficult to interpret, but can have high indirect
effects on the model’s logits. As we cannot interpret them, we exclude them from annotation and
from the SHIFT analysis (i.e., we do not ablate them). We also exclude them when running the
featureskylinein§4.
C FEATURE CIRCUITS
C.1 SUBJECT-VERBAGREEMENT
Here, we present the full agreement circuits for various syntactic agreement structures, with
researcher-provided annotations for features. We chose thresholds manually in order to keep the
numberofnodestoannotatemanageablewhilestilldisplayingthefullrangeoffeaturetypesfora
giventask.
Ineachcircuit,sparsefeaturesareshowninrectangles,whereascausallyrelevanterrortermsnotyet
capturedbyourSAEsareshownintriangles. Nodesshadedindarkercolorshavestrongereffects
on the target metric m. Blue nodes and edges are those which have positive indirect effects (i.e.,
are useful for performing the task correctly), whereas red nodes and edges are those which have
counterproductiveeffectsonm(i.e.,causethemodeltoconsistentlypredictincorrectanswers).
First,wepresentagreementacrossarelativeclause. Pythia(Figure7)andGemma(Figure8)both
appeartodetectthesubject’sgrammaticalnumberatthesubjectposition.Onepositionlater,features
detectthepresenceofrelativepronouns(thestartofthedistractorclause). Finally,atthelasttoken
oftherelativeclause,theattentionmovesthesubjectinformationtothelastposition,whereitassists
inpredictingthecorrectverbinflection. Gemma2additionallyleveragesnounphrase(NP)number
trackingfeatures,whichareactiveatallpositionsforNPsofagivennumber(exceptondistractor
phrasesofoppositenumber). WepresentanexampleofanNPnumbertrackerfeatureinFigure15.
Thecircuitsforagreementacrossaprepositionalphrase(Figures9and10)lookremarkablysimilar
toagreementacrossarelativeclause;forbothPythiaandGemma,thesetwocircuitsshareover85%
3Inotherwords,theaveragenumberoffeaturesactiveforagiventoken.
22

PublishedasaconferencepaperatICLR2025
Layer %VarianceExplained L1 L0 %Alive CEDiff %CERecovered
Resid0 92% 11 59 41% 0.24 97%
Resid1 85% 13 54 38% 0.45 95%
Resid2 96% 24 108 27% 0.55 94%
Resid3 96% 23 68 22% 0.58 95%
Resid4 88% 23 61 27% 0.48 95%
Resid5 90% 35 72 45% 0.55 92%
Table6: Residual(Resid)SAEevaluationbylayer.
Figure7: ThefeaturecircuitforagreementacrossarelativeclauseinPythia-70M,computedusing
T = 0.1andT = 0.01. Themodeldetectsthesubject’snumberatthesubjectposition. Other
N E
featuresdetectrelativepronouns(thestartofthedistractorclause). Finally,atthelasttokenofthe
RC,theattentionmovesthesubjectinformationtothelastposition,whereitassistsinpredictingthe
correctverbinflection.
oftheirfeatures,andmanyofthesamefeaturesareusedfordetectingbothprepositionsandrelative
clauses.
Forsimpleagreement(Figures11and12),manyofthesamefeaturesthatwereimplicatedinnoun
number detection and verb number prediction in the previous circuits also appear here. The mod-
els detect the subject’s number at the subject position in early layers. In later layers, these noun
number detectors become inputs to verb number promoters, which activate on anything predictive
ofparticularverbinflections.
The circuits for agreement within a relative clause (Figures 13 and 14) appear to have the same
structure as that for simple agreement: subject number detectors in early layers, followed by verb
numberpromotersinlaterlayers.
C.2 BIASINBIOSCIRCUIT
Here,wepresentthefullannotatedcircuitdiscoveredfortheBiasinBiosclassifiertrainedonPythia-
70M (described in §4 and App. E). The circuit was discovered using T = 0.1 and T = 0.01.
N E
We observe that the circuit (Figure 16) contains many nodes which simply detect the presence of
genderedpronounsorgenderednames. Afewfeaturesattendtoprofessioninformation,including
onewhichactivatesonwordsrelatedtonursing,andanotherwhichactivatesonpassagesrelatingto
scienceandacademia.
C.3 CLUSTERCIRCUITS
Here, we present full annotated circuits discovered for automatically discovered behaviors (de-
scribed in App. G). First, we present the circuit for incrementing number sequences (Figure 17),
discoveredwithT = 0.4andT = 0.04. Wenotethatthiscircuitincludesmanyfeatureswhich
N E
perform either succession (Gould et al., 2023) or induction (Olsson et al., 2022). The succession
23

PublishedasaconferencepaperatICLR2025
Figure8:ThefeaturecircuitforagreementacrossarelativeclauseinGemma-2-2B,computedusing
T =0.073andT =0.007.
N E
24

PublishedasaconferencepaperatICLR2025
Figure9: ThefeaturecircuitforagreementacrossaprepositionalphraseinPythia-70M,computed
using T = 0.1 and T = 0.01. The model detects the subject’s number at the subject position.
N E
Other features detect prepositional phrases (the start of the distractor clause). Finally, at the last
tokenoftheRC,theattentionmovesthesubjectinformationtothelastposition,whereitassistsin
predictingthecorrectverbinflection.
Figure 10: The feature circuit for agreement across a prepositional phrase in Gemma-2-2B, com-
putedusingT = 0.5andT = 0.05. Notethatweshowthecircuitbeginninginlayer13,asour
N E
circuitdiscoveryimplicatedonlyonenodeinearlierlayers.
25

PublishedasaconferencepaperatICLR2025
Figure 11: The feature circuit for simple agreement in Pythia-70M, computed using T = 0.2
N
and T = 0.02. The model detects the subject’s number at the subject position in early layers.
E
Inlaterlayers, theseareinputstofeatureswhichactivateonanythingpredictiveofparticularverb
inflections.
features in the layer 3 attention seem to be general; they increment many different numbers and
letters (as in Figure 5). The induction features are sensitive only to specific tokens: for example,
contextsoftheform“x3...x3”, where“3”isaliteral. Thesecomposetoformspecificsuccessor
featuresinlayer5: themoststrongly-activatinglayer5residualfeaturespecificallyincrements“3”
to“4”giveninduction-likelists,whereeachlistitemisprecededbythesamestring(e.g.,“Chapter
1...Chapter2...Chapter3...Chapter”).
Thecircuitforpredictinginfinitivalobjects(Figure18,discoveredwithT =0.25andT =0.001)
N E
contains twodistinct mechanisms. First, the model detects the presence ofspecific verbs like “re-
member”or“require”whichoftentakeinfinitivalobjects. Then,themodelusestwoseparatemech-
anisms to predict infinitive objects. The first mechanism detects present-tense verbs, participles,
orpredicateadjectiveswhichcanbeimmediatelyfollowedbyinfinitivaldirectobjects(e.g.,“They
were excited to...”). The second mechanism detects nominal direct objects that can directly pre-
cede infinitival object complements (e.g., “They asked us to...”). Finally, these two mechanisms
bothinfluencetheoutputinlayer5withoutfullyintersecting.
D SAMPLE FEATURES
D.1 SPARSEFEATURES
Here, we present examples of sparse features with high indirect effects on the Bias in Bios task.
Someofthesefeaturesclearlyactivateontermsrelatedtomedicineoracademia,whicharerelated
to the target profession classification task. Others simply detect the presence of “he” or female
names.
D.2 NEURONS
For contrast, we also present examples of dense features—that is, neurons from MLPs, layer-end
residuals, and the out-projection of the attention—with high indirect effects on the Bias in Bios
task. We cannot directly interpret the activation patterns of these neurons, and so it is difficult to
26

PublishedasaconferencepaperatICLR2025
Figure12:ThefeaturecircuitforsimpleagreementinGemma-2-2B,computedusingT =0.5and
N
T =0.05.
E
27

PublishedasaconferencepaperatICLR2025
Figure13: ThefeaturecircuitforagreementwithinarelativeclauseinPythia-70M,computedwith
T = 0.2 and T = 0.02. The model detects the subject’s number at the subject (within the
N E
RC)’spositioninearlylayers. Inlaterlayers,thesefeaturesareinputstofeatureswhichactivateon
anythingpredictiveofparticularverbinflections.
run the SHIFT with neurons baseline. We therefore instead compare to the neuron skyline, where
weallowtheskylineanunfairadvantagebysimplyablatingneuronswhichhavepositiveeffectson
gender-basedprobabilitiesgiventhebalancedset.
E IMPLEMENTATION DETAILS FOR CLASSIFIER EXPERIMENTS
E.1 CLASSIFIERTRAINING
HerewedescribehowwetrainlinearclassificationheadsonPythia-70MandGemma-2-2BtheBias
inBios(BiB)taskof§4.
GivenamodelM andchoiceℓoflayer,wemean-poolover(non-padding)tokensalllayerℓresidual
stream activations from M; we then train a linear classification head via logistic regression, using
the AdamW optimizer (Loshchilov & Hutter, 2017) and learning rate 0.01 for one epoch on this
datasetofactivations. Theactivationsandlabelsforthislogisticregressionarecollectedfromthe
ambiguoussetforthebaselineclassifierandfromthebalancedsetfortheoracleclassifier.
To mimick a realistic application setting, we tune the choice ℓ of layer for the baseline probe’s
accuracyon(atestsplitof)theambiguousset. ForPythia,thisrecommendsusingthepenultimate
layer ℓ = 4. For Gemma, there is a wide range of equally performant layers. Thus—for this one
choiceonly—wemakeuseofthebalancedsettocomputehowthebaselineprobegeneralizes;we
select the layer ℓ = 22 for which the baseline probe generalizes worst. We make this choice to
setupatestbedwherethereisthemostspaceforimprovement. Weemphasizethatwenevertune
hyperparametersfortheperformancebalancedsetofSHIFT,asusingthebalancedsetisforbidden
bytheproblemstatement.
Whenretrainingafterperforming SHIFT,weretrainonlythelinearclassificationhead,notthefull
model.
28

PublishedasaconferencepaperatICLR2025
Figure 14: The feature circuit for agreement within a relative clause for Gemma-2-2B, computed
withT =0.5andT =0.05.
N E
Figure 15: An example sparse feature for agreement across a relative clause in Gemma 2
(resid 12/13561). Thisfeatureactivatesontokensinnounphraseswherethenounheadisplural,
but not on singular distractor phrases within the plural NP. This feature carries the number of the
subjectacrosspositions,sowetermitan“NPnumbertracker”.
29

PublishedasaconferencepaperatICLR2025
Figure 16: The full annotated feature circuit for the Bias in Bios classifier. Many nodes simply
detectthepresenceofgenderedpronounsorgenderednames. Afewfeaturesattendtoprofession
information,includingonewhichactivatesonwordsrelatedtonursing,andanotherwhichactivates
onpassagesrelatingtoscienceandacademia.
Figure 17: The full annotated feature circuit for incrementing number sequences. The model first
detects the presence of specific number tokens, like “3”. Later, it learns more robust semantic
representations of those numbers, like “iii” and “Three”. Then, the model uses a series of narrow
andgeneralsuccesionandinductionfeaturestoincrementthenextnumber.
30

PublishedasaconferencepaperatICLR2025
Figure18: Thefullannotatedfeaturecircuitforpredicting“to”asaninfinitivalobject. Themodel
first detects the presence of verbs that often take infinitival objects. Then, it uses one mechanism
todetectpresent-tenseverbs, participles, orpredicateadjectiveswhichtakeinfinitivalobjects, and
anothermechanismtodetectdirectobjectsthatcandirectlyprecedeinfinitivalobjectcomplements.
Finally,thesetwomechanismsbothinfluencetheoutputinlayer5withoutfullyintersecting.
Figure 19: An example sparse feature from the Bias in Bios task (attn 3/22029). This feature
detectsfemale-relatedwordsinbiographiesofwomen. Italsopromoteswordslike“husband”and
“ne´e”. This feature probably contributes to preferences for the spurious correlate of gender; we
thereforeablateit.
Figure 20: An example sparse feature from the Bias in Bios task (resid 2/31098). This feature
activates on words related to nursing, including “RN” and “nurse”. This probably relates to the
targettaskofprofessionprediction. Wethereforekeepit.
31

PublishedasaconferencepaperatICLR2025
Figure21: AnexampleneuronfromtheBiasinBiostask. Thisappearstoactivateonbeginnings
andendsofsentences,butalsomorestronglyonanytokeninasentencethatcontainscapitalletters
ornumbers. Wecannotdeducewhetherthiswouldcontributemoretogenderorprofessionnames.
Figure22:AnexampleneuronfromtheBiasinBiostask.Thisactivatespositivelyontokensstarting
withcapitalletters,butnegativelyonmanyothertokens(whoseunifyingthemewecannotdeduce).
E.2 IMPLEMENTATIONFORCONCEPTBOTTLENECKPROBING
Our implementation for Concept Bottleneck Proving (CBP) is adapted from (Yan et al., 2023). It
worksasfollows:
1. First, we collect a number of keywords related to the intended prediction task. We use
N =20keywords: nurse,healthcare,hospital,patient,medical,clinic,triage,medication,
emergency,surgery,professor,academia,research,university,tenure,faculty,dissertation,
sabbatical,publication,andgrant.
2. Weobtainconceptvectorsc ,...,c foreachkeywordbyextractingPythia-70M’spenul-
1 N
timatelayerrepresentationoverthefinaltokenofeachkeyword, andthensubtractingoff
themeanconceptvector. (Withoutthisnormalization,wefoundthatconceptvectorshave
veryhighpairwisecosinesimilarities.)
3. Given an input with representation x (obtained via the mean-pooling procedure in
App. E.1), we obtain a concept bottleneck representation z ∈ RN by taking the cosine
similaritywitheachc .
i
4. Finally,wetrainalinearprobewithlogisticregressionontheconceptbottleneckrepresen-
tationsz,asinApp.E.1.
Wedecidedtonormalizeconceptvectorsbutnotinputrepresentationsbecauseitresultedinstronger
performance. Wealsoexperimentedwithcomputingcosinesimilaritiesbeforemeanpooling.
F HUMAN INTERPRETABILITY RATINGS FOR SPARSE FEATURES
Given our trained Pythia-70M sparse autoencoders, we asked human crowdworkers to rate the in-
terpretability of random features, random neurons, features from our feature circuits, and neurons
fromourneuroncircuitsona0–100scale(Table7). Crowdworkersratesparsefeaturesassignifi-
cantlymoreinterpretablethanneurons,withfeaturesthatparticipateinourcircuitsalsobeingmore
interpretablethanrandomlysampledfeatures.
32

PublishedasaconferencepaperatICLR2025
Activationtype Interpretability
Dense(random) 32.6
Dense(agreement) 30.2
Dense(BiB) 36.0
Sparse(random) 52.8
Sparse(agreement) 62.3
Sparse(BiB) 81.5
Table 7: Human interpretability ratings for dense (neuron) vs. sparse (autoencoder) features. We
presentmeaninterpretabilityscoresacrossfeaturesona0–100scale. Weshowscoresforfeatures
that were either uniformly sampled (random), the top 30 by IˆE from the subject-verb agreement
acrossRCtask(agreement;§3.3),orthetop30byIˆEfortheBiasinBiostask(BiB;§4).
Figure 23: The human annotation interface used to obtain the interpretability ratings in Table 7.
Here,weshowtheinstructions,top-activatingtokens,thetokenprobabilitiesthatweremostaffected
whenablatingthefeature,andexamplecontextswithfeatureactivationvalues.
33

PublishedasaconferencepaperatICLR2025
Figure 24: The human annotation interface used to obtain the interpretability ratings in Table 7.
Here, we show the rating interface on the same page as the content in Fig. 23, below the example
contexts. Humans were asked to write a textual description of each feature, assign a 0–100 inter-
pretabilityrating,andassigna0–100semanticcomplexityratingtoeachfeature.
SeeFigures23and24forexamplesofthehumanannotatorinterface. Humanswerepresentedwith
thetokensonwhichthefeatureactivatedmoststrongly,followedbythetokenswhoseprobabilities
were most affected in Pythia-70M when the feature was ablated. This is followed by a series of
examplecontextsinwhichthefeatureactivatedonsomesubsetoftokens,wherefeatureactivations
areshowninvaryingshadesofblue(darkershadesindicatehigheractivations). Onthesamepage
belowthecontexts,weaskannotatorstowriteatextualdescriptionofthefeature,andratebothits
interpretabilityanditssemanticcomplexityon0–100scales.
CrowdworkerswererecruitedfromtheARENASlackchannel,whosemembersaremachinelearn-
ing researchers interested in AI alignment and safety. The selection of annotators certainly influ-
encedourresults;atrulyrandomsampleofhumanannotatorswouldlikelydisplayhighervariance
whenannotatingfeatures.
One common error pattern we notice is that annotators often label features according to semantic
groupings (e.g., “text about politics,” and do not pay attention to syntactic context (e.g., “plural
nouns”). Futureworkcouldaddressthisdesignbiasbytestingvariantsoftheinstructions.
ResultsofhumanevaluationsfortheGemmaScopeSAEsaredescribedinLieberumetal.(2024).
G DISCOVERING LM BEHAVIORS WITH CLUSTERING
In this section, we describe our unsupervised method for discovering language model behaviors.
Morespecifically,followingMichaudetal.(2023),weclustercontextsfromThePileaccordingto
thePythia-70M’sinternalstateduringinference. Inthissection,wedescribeourclusteringpipeline
andmethods.
G.1 FILTERINGTOKENS
We must first locate (context, answer) pairs for which an LM correctly predicts the answer token
fromthecontext. WeselectThePile(Gaoetal.(2020))asageneraltextcorpusandfiltertopairs
onwhichPythia-70Mconfidentlyandcorrectlypredictstheanswertoken,withcross-entropylower
than 0.1 or 0.3 nats, depending on the experiment. The model consistently achieves low loss on
tokenswhichinvolve“induction”(Olssonetal.,2022)—i.e.,tokenswhicharepartofasubsequence
34

PublishedasaconferencepaperatICLR2025
which occurred earlier in the context. We exclude induction samples by filtering out samples in
whichthebigram(finalcontexttoken,answertoken)occuredearlierinthecontext.
G.2 CACHINGMODEL-INTERNALINFORMATION
We find behaviors by clustering samples according to information about the LM’s internals when
runonthatsample. Wefindclustersofsampleswherethemodelemployssimilarmechanismsfor
next-tokenprediction. Weexperimentwithvariousinputstotheclusteringalgorithm:
• DenseActivations: Wetakeactivations(residualstreamvectors, attentionblockoutputs,
or MLP post-activations) from a given context and concatenate them. To obtain a vector
whoselengthisindependentofthecontextlength,wecaneitherusetheactivationsatthe
lastN contextpositionsbeforetheanswertoken, oraggregate(sum)acrossthesequence
dimension. Weexperimentwithbothvariants.
• Sparse Activations: Rather than dense model activations, we can use the activations of
SAEfeatures. Weconcatenateandaggregatetheseinthesamemannerasfordenseactiva-
tions.
• DenseComponentIndirectEffects: Weapproximatetheindirecteffectofallfeatureson
thecorrectpredictionusing2withoutacontrastivepair—namely,bysettinga =0.The
patch
negativelog-probabilityoftheanswertokenm=−logp(answer)servesasourmetricfor
thecorrectpredictionofthenexttoken. Thecomputatiomoflineareffectsrequiressaving
both(1)activationsand(2)gradientsw.r.tmatthefinalN positionsforeachcontextinthe
dataset. Weoptionallyaggregatebysummingoverallpositions.
• SparseIndirectEffects:Similarly,wecancomputethelineareffectsofsparseactivations
onthecorrectprediction.
• Gradientw.r.t.modelparameters: AsinMichaudetal.(2023),wealsoexperimentwith
using gradients of the loss w.r.t. model parameters, but with some modifications. We de-
scribethismethodinmoredetailin§G.3below.
G.3 HYPERPARAMETERSANDIMPLEMENTATIONDETAILS
We apply either spectral clustering or k-means clustering. For spectral clustering, given ei-
ther activations or effects x for sample i, we compute a matrix of pairwise cosine similarities
i
C = x ·x /(||x ||||x ||) between all pairs of samples. Before performing spectral clustering,
ij i j i j
wenormalizeallelementsofC tobein[0,1]byconvertingthecosinesimilaritiestoangularsimi-
larities: Cˆ =1−arccos(C )/π.
ij ij
Weusethescikit-learn(Pedregosaetal.,2011)spectralclusteringimplementationwithk-means.
For all inputs except gradients w.r.t. model parameters, we used spectral clustering across 8192
samples. Wechosek (thenumberoftotalclusters)tomaximizethenumberofclustersimplicated
inmorethanoneinputcontext.
We also experimented with using gradients w.r.t. model parameters as inputs, as in Michaud et al.
(2023). Here, we scale up our approach to 100,000 samples. It is intractible to perform spectral
clustering given 100,000 samples, so we instead use k-means clustering. Rather than clustering
thegradientsthemselves(whicharehigh-dimensional),weclustersparserandomprojectionsofthe
gradients down to 30,000 dimensions. When projecting, we use a matrix with entries {−1,0,1}.
Whensamplingtheentriesofthismatrix, sampleanonzerovaluewithprobability32/30000, and
ifnonzero,sample−1or1withequalprobability. Forasparseprojectionmatrixwithdimensions
Rn×30000,therewillonaveragebe32·nnonzeroentries,wherenisthenumberofparametersin
themodel.4
H QUALITY OF LINEAR APPROXIMATIONS OF INDIRECT EFFECTS
Figure 25 shows the quality of our linear approximations for indirect effects. Prior work (Nanda,
2022;Krama´retal.,2024)investigatedattributionpatchingaccuracyforIEsofcoarse-grainedmodel
4Weonlyconsidergradientsw.r.t.non-embeddingandnon-layernormparameters.
35

PublishedasaconferencepaperatICLR2025
m
Residual
strea
Attention
MLP
Exact effect (IE)
)Ê
I(
tceffe
etamixorppA
(a) Attribution patching
Layer 0 Layer 1 Layer 2 Layer 3 Layer 4 Layer 5 Layer 6
m
Residual
strea
Attention
MLP
SAE feature
(b) Integrated gradients
SAE error
Layer 0 Layer 1 Layer 2 Layer 3 Layer 4 Layer 5 Layer 6
Figure 25: Approximate IEs (y-axis) and exact IEs (x-axis) using attribution patching (a; top) or
integrated gradients (b; bottom). Each point corresponds to an SAE feature or SAE error at one
tokenpositionofoneinput. Datawerecollectedfrom30inputsfromouracrossRCdataset.
components (queries, keys, and values for attention heads, residual stream vectors, and MLP out-
puts)andMLPneurons. WorkingwithSAEfeaturesanderrors,ourresultsechopreviousfindings:
attributionpatchingisgenerallyquitegood,butsometimesunderestimatesthetrueIEs. Notableex-
ceptionsarethelayer0MLPandtheresidualstreaminearlylayers. Wealsofindthatourintegrated
gradients-basedapproximationsignificantlyimprovesapproximationquality.
36