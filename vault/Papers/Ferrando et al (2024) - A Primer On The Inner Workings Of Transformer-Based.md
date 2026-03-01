---
title: "A Primer On The Inner Workings Of Transformer-Based Language Models"
authors: ["Ferrando, Javier", "Sarti, Gabriele", "Bisazza, Arianna", "Costa-Jussà, Marta R", "Abnar, S", "Zuidema, W", "Adebayo, J", "Gilmer, J", "Muelly, M", "Goodfellow, I", "Hardt, M", "Kim, B", "Adebayo, J", "Muelly, M", "Liccardi, I", "Kim, B", "Adebayo, J", "Muelly, M", "Abelson, H", "Kim, B", "Ahmadian, A", "Dash, S", "Chen, H", "Venkitesh, B", "Gou, Z S", "Blunsom, P", "Üstün, A", "Hooker, S", "Akyurek, E", "Bolukbasi, T", "Liu, F", "Xiong, B", "Tenney, I", "Andreas, J", "Guu, K", "Akyürek, E", "Schuurmans, D", "Andreas, J", "Ma, T", "Zhou, D", "Alain, G", "Bengio, Y", "Alammar, J", "Ali, A", "Schnake, T", "Eberle, O", "Montavon, G", "Müller, K.-R", "Wolf, L", "Anil, C", "Wu, Y", "Andreassen, A J", "Lewkowycz, A", "Misra, V", "Ramasesh, V V", "Slone, A", "Gur-Ari, G", "Dyer, E", "Neyshabur, B", "Arditi, A", "Obeso, O", "Syed, A", "Paleka, D", "Rimsky, N", "Gurnee, W", "Nanda, N", "Arora, S", "Li, Y", "Liang, Y", "Ma, T", "Risteski, A", "Atanasova, P", "Simonsen, J G", "Lioma, C", "Augenstein, I", "Atanasova, P", "Camburu, O.-M", "Lioma, C", "Lukasiewicz, T", "Simonsen, J G", "Augenstein, I", "Attanasio, G", "Pastor, E", "Bonaventura, C Di", "Nozza, D", "Avitan, M", "Cotterell, R", "Goldberg, Y", "Ravfogel, S", "Azaria, A", "Mitchell, T", "Ba, J L", "Kiros, J R", "Hinton, G E", "Bach, S", "Binder, A", "Montavon, G", "Klauschen, F", "Müller, K.-R", "Samek, W", "Bai, Y", "Jones, A", "Ndousse, K", "Askell, A", "Chen, A", "Dassarma, N", "Drain, D", "Fort, S", "Ganguli, D", "Henighan, T", "Joseph, N", "Kadavath, S", "Kernion, J", "Conerly, T", "El-Showk, S", "Elhage, N", "Hatfield-Dodds, Z", "Hernandez, D", "Hume, T", "Johnston, S", "Kravec, S", "Lovitt, L", "Nanda, N", "Olsson, C", "Amodei, D", "Brown, T", "Clark, J", "Mc-Candlish, S", "Olah, C", "Mann, B", "Kaplan, J", "Balduzzi, D", "Frean, M", "Leary, L", "Lewis, J P", "Ma, -D", "Mcwilliams, B", "Bastings, J", "Filippova, K", "Bastings, J", "Ebert, S", "Zablotskaia, P", "Sandholm, A", "Filippova, K", "Bau, A", "Belinkov, Y", "Sajjad, H", "Durrani, N", "Dalvi, F", "Glass, J", "Bau, D", "Zhu, J.-Y", "Strobelt, H", "Lapedriza, A", "Zhou, B", "Torralba, A", "Belinkov, Y", "Belinkov, Y", "Glass, J", "Belinkov, Y", "Durrani, N", "Dalvi, F", "Sajjad, H", "Glass, J", "Belrose, N", "Belrose, N", "Furman, Z", "Smith, L", "Halawi, D", "Ostrovsky, I", "Mckinney, L", "Biderman, S", "Steinhardt, J", "Belrose, N", "Schneider-Joseph, D", "Ravfogel, S", "Cotterell, R", "Raff, E", "Biderman, S", "Bengio, Y", "Ducharme, R", "Vincent, P", "Janvin, C", "Bereska, L", "Gavves, E", "Bibal, A", "Cardon, R", "Alfter, D", "Wilkens, R", "Wang, X", "François, T", "Watrin, P", "Biderman, S", "Schoelkopf, H", "Anthony, Q", "Bradley, H", "O'brien, K", "Hallahan, E", "Khan, M A", "Purohit, S", "Prashanth, U S", "Raff, E", "Skowron, A", "Sutawika, L", "Van Der Wal, O", "Bietti, A", "Cabannes, V", "Bouchacourt, D", "Jegou, H", "Bottou, L", "Bilodeau, B", "Jaques, N", "Koh, P W", "Kim, B", "Bloom, J", "Lin, J", "Bondarenko, Y", "Nagel, M", "Blankevoort, T", "Bricken, T", "Templeton, A", "Batson, J", "Chen, B", "Jermyn, A", "Conerly, T", "Turner, N", "Anil, C", "Denison, C", "Askell, A", "Lasenby, R", "Wu, Y", "Kravec, S", "Schiefer, N", "Maxwell, T", "Joseph, N", "Hatfield-Dodds, Z", "Tamkin, A", "Nguyen, K", "Mclean, B", "Burke, J E", "Hume, T", "Carter, S", "Henighan, T", "Olah, C", "Brody, S", "Alon, U", "Yahav, E", "Brown, T", "Mann, B", "Ryder, N", "Subbiah, M", "Kaplan, J D", "Dhariwal, P", "Neelakantan, A", "Shyam, P", "Sastry, G", "Askell, A", "Agarwal, S", "Herbert-Voss, A", "Krueger, G", "Henighan, T", "Child, R", "Ramesh, A", "Ziegler, D", "Wu, J", "Winter, C", "Hesse, C", "Chen, M", "Sigler, E", "Litwin, M", "Gray, S", "Chess, B", "Clark, J", "Berner, C", "Mccandlish, S", "Radford, A", "Sutskever, I", "Amodei, D", "Brunet, M.-E", "Alkalay-Houlihan, C", "Anderson, A", "Zemel, R", "Brunner, G", "Liu, Y", "Pascual, D", "Richter, O", "Ciaramita, M", "Wattenhofer, R", "Burns, C", "Ye, H", "Klein, D", "Steinhardt, J", "Chefer, H", "Gur, S", "Wolf, L", "Chen, A", "Shwartz-Ziv, R", "Cho, K", "Leavitt, M L", "Saphra, N", "Chen, C", "Liu, K", "Chen, Z", "Gu, Y", "Wu, Y", "Tao, M", "Fu, Z", "Ye, J", "Chowdhery, A", "Narang, S", "Devlin, J", "Bosma, M", "Mishra, G", "Roberts, A", "Barham, P", "Chung, H W", "Sutton, C", "Gehrmann, S", "Schuh, P", "Shi, K", "Tsvyashchenko, S", "Maynez, J", "Rao, A", "Barnes, P", "Tay, Y", "Shazeer, N", "Prabhakaran, V", "Reif, E", "Du, N", "Hutchinson, B", "Pope, R", "Bradbury, J", "Austin, J", "Isard, M", "Gur-Ari, G", "Yin, P", "Duke, T", "Levskaya, A", "Ghemawat, S", "Dev, S", "Michalewski, H", "Garcia, X", "Misra, V", "Robinson, K", "Fedus, L", "Zhou, D", "Ippolito, D", "Luan, D", "Lim, H", "Zoph, B", "Spiridonov, A", "Sepassi, R", "Dohan, D", "Agrawal, S", "Omernick, M", "Dai, A M", "Pillai, T S", "Pellat, M", "Lewkowycz, A", "Moreira, E", "Child, R", "Polozov, O", "Lee, K", "Zhou, Z", "Wang, X", "Saeta, B", "Diaz, M", "Firat, O", "Catasta, M", "Wei, J", "Meier-Hellstern, K", "Eck, D", "Dean, J", "Petrov, S", "Fiedel, N", "Chuang, Y.-S", "Xie, Y", "Luo, H", "Kim, Y", "Glass, J R", "He, P", "Clark, K", "Khandelwal, U", "Levy, O", "Manning, C D", "Conerly, T", "Templeton, A", "Bricken, T", "Marcus, J", "Henighan, T", "Conmy, A", "Mavor-Parker, A", "Lynch, A", "Heimersheim, S", "Garriga-Alonso, A", "Correia, G M", "Niculae, V", "Martins, A F T", "Costa-Jussà, M", "Smith, E", "Ropers, C", "Licht, D", "Maillard, J", "Ferrando, J", "Escolano, C", "Covert, I", "Lundberg, S", "Lee, S.-I", "Crabbé, J", "Van Der Schaar, M", "Csordás, R", "Van Steenkiste, S", "Schmidhuber, J", "Cunningham, H", "Ewart, A", "Riggs, L", "Huben, R", "Sharkey, L", "Dai, D", "Dong, L", "Hao, Y", "Sui, Z", "Chang, B", "Wei, F", "Dale, D", "Voita, E", "Barrault, L", "Costa-Jussà, M R", "Dale, D", "Voita, E", "Lam, J", "Hansanti, P", "Ropers, C", "Kalbassi, E", "Gao, C", "Barrault, L", "Costa-Jussà, M", "Dalvi, F", "Durrani, N", "Sajjad, H", "Belinkov, Y", "Bau, A", "Glass, J", "Dar, G", "Geva, M", "Gupta, A", "Berant, J", "Darcet, T", "Oquab, M", "Mairal, J", "Bojanowski, P", "Dauphin, Y N", "Fan, A", "Auli, M", "Grangier, D", "De Cao, N", "Schlichtkrull, M S", "Aziz, W", "Titov, I", "De Cao, N", "Aziz, W", "Titov, I", "De Cao, N", "Schmid, L", "Hupkes, D", "Titov, I", "Deiseroth, B", "Deb, M", "Weinbach, S", "Brack, M", "Schramowski, P", "Kersting, K", "Denil, M", "Demiraj, A", "De Freitas, N", "Dettmers, T", "Lewis, M", "Belkada, Y", "Zettlemoyer, L", "Devlin, J", "Chang, M.-W", "Lee, K", "Toutanova, K", "Deyoung, J", "Jain, S", "Rajani, N F", "Lehman, E", "Xiong, C", "Socher, R", "Wallace, B C", "Dhamdhere, K", "Sundararajan, M", "Yan, Q", "Dhanorkar, S", "Wolf, C T", "Qian, K", "Xu, A", "Popa, L", "Li, Y", "Din, A Y", "Karidi, T", "Choshen, L", "Geva, M", "Ding, S", "Koehn, P", "Toutanova, K", "Rumshisky, A", "Zettlemoyer, L", "Hakkani-Tur, D", "Beltagy, I", "Bethard, S", "Durrani, N", "Dalvi, F", "Sajjad, H", "Elazar, Y", "Ravfogel, S", "Jacovi, A", "Goldberg, Y", "Elhage, N", "Nanda, N", "Olsson, C", "Henighan, T", "Joseph, N", "Mann, B", "Askell, A", "Bai, Y", "Chen, A", "Conerly, T", "Dassarma, N", "Drain, D", "Ganguli, D", "Hatfield-Dodds, Z", "Hernandez, D", "Jones, A", "Kernion, J", "Lovitt, L", "Ndousse, K", "Amodei, D", "Brown, T", "Clark, J", "Kaplan, J", "Mccandlish, S", "Olah, C", "Elhage, N", "Lasenby, R", "Olah, C", "Enguehard, J", "Erichson, N B", "Yao, Z", "Mahoney, M W", "Ethayarajh, K", "Ethayarajh, K", "Jurafsky, D", "Fantozzi, P", "Naldi, M", "Feldhus, N", "Hennig, L", "Nasert, M D", "Ebert, C", "Schwarzenberg, R", "Möller, S", "Ferrando, J", "Costa-Jussà, M R", "Ferrando, J", "Gállego, G I", "Alastruey, B", "Escolano, C", "Costa-Jussà, M R", "Ferrando, J", "Gállego, G I", "Costa-Jussà, M R", "Ferrando, J", "Gállego, G I", "Tsiamas, I", "Costa-Jussà, M R", "Fierro, C", "Søgaard, A", "Fomicheva, M", "Sun, S", "Yankovskaya, L", "Blain, F", "Guzmán, F", "Fishel, M", "Aletras, N", "Chaudhary, V", "Specia, L", "Friedman, D", "Wettig, A", "Chen, D", "Geiger, A", "Richardson, K", "Potts, C", "Geiger, A", "Lu, H", "Icard, T", "Potts, C", "Team, G Gemma", "Mesnard, T", "Hardin, C", "Dadashi, R", "Bhupatiraju, S", "Pathak, S", "Sifre, L", "Rivière, M", "Kale, M S", "Love, J", "Tafti, P", "Hussenot, L", "Sessa, P G", "Chowdhery, A", "Roberts, A", "Barua, A", "Botev, A", "Castro-Ros, A", "Slone, A", "Héliou, A", "Tacchetti, A", "Bulanova, A", "Paterson, A", "Tsai, B", "Shahriari, B", "Lan, C L", "Choquette-Choo, C A", "Crepy, C", "Cer, D", "Ippolito, D", "Reid, D", "Buchatskaya, E", "Ni, E", "Noland, E", "Yan, G", "Tucker, G", "Muraru, G.-C", "Rozhdestvenskiy, G", "Michalewski, H", "Tenney, I", "Grishchenko, I", "Austin, J", "Keeling, J", "Labanowski, J", "Lespiau, J.-B", "Stanway, J", "Brennan, J", "Chen, J", "Ferret, J", "Chiu, J", "Mao-Jones, J", "Lee, K", "Yu, K", "Millican, K", "Sjoesund, L L", "Lee, L", "Dixon, L", "Reid, M", "Mikuła, M", "Wirth, M", "Sharman, M", "Chinaev, N", "Thain, N", "Bachem, O", "Chang, O", "Wahltinez, O", "Bailey, P", "Michel, P", "Yotov, P", "Chaabouni, R", "Comanescu, R", "Jana, R", "Anil, R", "Mcilroy, R", "Liu, R", "Mullins, R", "Smith, S L", "Borgeaud, S", "Girgin, S", "Douglas, S", "Pandya, S", "Shakeri, S", "De, S", "Klimenko, T", "Hennigan, T", "Feinberg, V", "Stokowiec, W", "Hui Chen, Y", "Ahmed, Z", "Gong, Z", "Warkentin, T", "Peran, L", "Giang, M", "Farabet, C", "Vinyals, O", "Dean, J", "Kavukcuoglu, K", "Hassabis, D", "Ghahramani, Z", "Eck, D", "Barral, J", "Pereira, F", "Collins, E", "Joulin, A", "Fiedel, N", "Senter, E", "Andreev, A", "Kenealy, K", "Gemma", "Geva, M", "Schuster, R", "Berant, J", "Levy, O", "Geva, M", "Caciularu, A", "Dar, G", "Roit, P", "Sadde, S", "Shlain, M", "Tamir, B", "Goldberg, Y", "Geva, M", "Caciularu, A", "Wang, K", "Goldberg, Y", "Geva, M", "Bastings, J", "Filippova, K", "Globerson, A", "Ghandeharioun, A", "Caciularu, A", "Pearce, A", "Dixon, L", "Geva, M", "Goldowsky-Dill, N", "Macleod, C", "Sato, L", "Arora, A", "Gould, R", "Ong, E", "Ogden, G", "Conmy, A", "Guerreiro, N M", "Colombo, P", "Piantanida, P", "Martins, A", "Guerreiro, N M", "Voita, E", "Martins, A", "Gupta, A", "Boleda, G", "Baroni, M", "Padó, S", "Gurnee, W", "Tegmark, M", "Gurnee, W", "Nanda, N", "Pauly, M", "Harvey, K", "Troitskii, D", "Bertsimas, D", "Guu, K", "Webson, A", "Pavlick, E", "Dixon, L", "Tenney, I", "Bolukbasi, T", "Han, X", "Wallace, B C", "Tsvetkov, Y", "Hanna, M", "Liu, O", "Variengien, A", "Hase, P", "Bansal, M", "Kim, B", "Ghandeharioun, A", "Haviv, A", "Cohen, I", "Gidron, J", "Schuster, R", "Goldberg, Y", "Geva, M", "Heimersheim, S", "Janiak, J", "Heimersheim, S", "Nanda, N", "Heimersheim, S", "Turner, A", "Hendel, R", "Geva, M", "Globerson, A", "Hernandez, E", "Sharma, A S", "Haklay, T", "Meng, K", "Wattenberg, M", "Andreas, J", "Belinkov, Y", "Bau, D", "Hewitt, J", "Liang, P", "Hewitt, J", "Manning, C D", "Hewitt, J", "Thickstun, J", "Manning, C", "Liang, P", "Hoffmann, J", "Borgeaud, S", "Mensch, A", "Buchatskaya, E", "Cai, T", "Rutherford, E", "De Las Casas, D", "Hendricks, L A", "Welbl, J", "Clark, A", "Hennigan, T", "Noland, E", "Millican, K", "Van Den Driessche, G", "Damoc, B", "Guy, A", "Osindero, S", "Simonyan, K", "Elsen, E", "Vinyals, O", "Rae, J", "Sifre, L", "Holtzman, A", "West, P", "Shwartz, V", "Choi, Y", "Zettlemoyer, L", "Hoover, B", "Strobelt, H", "Gehrmann, S", "Hu, P.-H", "Chang, R", "Luo, H.-Y", "Chen, W", "Li, W.-P", "Wang, H", "Liu", "Huang, J", "Geiger, A", "D'oosterlinck, K", "Wu, Z", "Potts, C", "Hudson, N", "Pauloski, J G", "Baughman, M", "Kamatar, A", "Sakarvadia, M", "Ward, L", "Chard, R", "Bauer, A", "Levental, M", "Wang, W", "Engler, W", "Skelly, O P", "Blaiszik, B", "Stevens, R", "Chard, K", "Foster, I", "Hupkes, D", "Veldhoen, S", "Zuidema, W", "Jain, S", "Kirk, R", "Lubana, E S", "Dick, R P", "Tanaka, H", "Rocktäschel, T", "Grefenstette, E", "Krueger, D", "Jain, S", "Wallace, B C", "Jermyn, A", "Templeton, A", "Ji, Z", "Lee, N", "Frieske, R", "Yu, T", "Su, D", "Xu, Y", "Ishii, E", "Bang, Y J", "Madotto, A", "Fung, P", "Joseph, S", "Kamradt, G", "Katz, S", "Belinkov, Y", "Kim, B", "Wattenberg, M", "Gilmer, J", "Cai, C", "Wexler, J", "Viegas, F", "Sayres, R", "Kissane, C", "Krzyzanowski, R", "Conmy, A", "Nanda, N", "Kobayashi, G", "Kuribayashi, T", "Yokoi, S", "Inui, K", "Kobayashi, G", "Kuribayashi, T", "Yokoi, S", "Inui, K", "Kobayashi, G", "Kuribayashi, T", "Yokoi, S", "Inui, K", "Kobayashi, G", "Kuribayashi, T", "Yokoi, S", "Inui, K", "Koh, P W", "Liang, P", "Köhn, A", "Kokhlikyan, N", "Miglani, V", "Martin, M", "Wang, E", "Alsallakh, B", "Reynolds, J", "Melnikov, A", "Kliushkina, N", "Araya, C", "Yan, S", "Reblitz-Richardson, O", "Kovaleva, A", "Romanov, A", "Rogers, A", "Rumshisky", "Kovaleva, S", "Kulshreshtha, A", "Rogers, A", "Rumshisky", "Krishna, S", "Han, T", "Gu, A", "Wu, S", "Jabbari, S", "Lakkaraju, H", "Krzyzanowski, R", "Kissane, C", "Conmy, A", "Nanda, N", "Kwon, Y", "Wu, E", "Wu, K", "Zou, J", "Lal, V", "Ma, A", "Aflalo, E", "Howard, P", "Simoes, A", "Korat, D", "Pereg, O", "Singer, G", "Wasserblat, M", "Leino, K", "Sen, S", "Datta, A", "Fredrikson, M", "Li, L", "Li, J", "Chen, X", "Hovy, E", "Jurafsky, D", "Li, K", "Patel, O", "Viégas, F", "Pfister, H", "Wattenberg, M", "Li, X L", "Holtzman, A", "Fried, D", "Liang, P", "Eisner, J", "Hashimoto, T", "Zettlemoyer, L", "Lewis, M", "Li, Z", "Zhang, N", "Yao, Y", "Wang, M", "Chen, X", "Chen, H", "Liao, V", "Gruen, D", "Miller, S", "Lieberum, T", "Rahtz, M", "Kramár, J", "Nanda, N", "Irving, G", "Shah, R", "Mikulik, V", "Lin, Y", "Tan, Y C", "Frank, R", "Lindner, D", "Kramar, J", "Farquhar, S", "Rahtz, M", "Mcgrath, T", "Mikulik, V", "Lipton, Z C", "Liu, N F", "Gardner, M", "Belinkov, Y", "Peters, M E", "Smith, N A", "Liu, Q", "Chai, Y", "Wang, S", "Sun, Y", "Wang, K", "Wu, H", "Longo, L", "Brcic, M", "Cabitza, F", "Choi, J", "Confalonieri, R", "Ser, J D", "Guidotti, R", "Hayashi, Y", "Herrera, F", "Holzinger, A", "Jiang, R", "Khosravi, H", "Lecue, F", "Malgieri, G", "Páez, A", "Samek, W", "Schneider, J", "Speith, T", "Stumpf, S", "Loog, M", "Viering, T", "Mey, A", "Krijthe, J H", "Tax, D M J", "Lundberg, S M", "Lee, S.-I", "Luo, Z", "Kulmizev, A", "Mao, X", "Lv, A", "Zhang, K", "Chen, Y", "Wang, Y", "Liu, L", "Wen, J.-R", "Xie, J", "Yan, R", "Madsen, A", "Reddy, S", "Chandar, S", "Makelov, A", "Lange, G", "Geiger, A", "Nanda, N", "Marks, S", "Rager, C", "Michaud, E J", "Belinkov, Y", "Bau, D", "Mueller, A", "Mccoy, T", "Pavlick, E", "Linzen, T", "Mcdougall, C", "Mcdougall, C", "Conmy, A", "Rushing, C", "Mcgrath, T", "Nanda, N", "Mcgrath, T", "Kapishnikov, A", "Tomašev, N", "Pearce, A", "Wattenberg, M", "Hassabis, D", "Kim, B", "Paquet, U", "Kramnik, V", "Mcgrath, T", "Rahtz, M", "Kramar, J", "Mikulik, V", "Legg, S", "Meng, K", "Bau, D", "Andonian, A", "Belinkov, Y", "Meng, K", "Sharma, A S", "Andonian, A J", "Belinkov, Y", "Bau, D", "Merrill, W", "Ramanujan, V", "Goldberg, Y", "Schwartz, R", "Smith, N A", "Merullo, J", "Eickhoff, C", "Pavlick, E", "Michel, P", "Levy, O", "Neubig, G", "Mickus, T", "Paperno, D", "Constant, M", "Miglani, V", "Yang, A", "Markosyan, A", "Garcia-Olano, D", "Kokhlikyan, N", "Mikolov, T", "Sutskever, I", "Chen, K", "Corrado, G S", "Dean, J", "Mitchell, E", "Lin, C", "Bosselut, A", "Finn, C", "Manning, C D", "Mitchell, E", "Lin, C", "Bosselut, A", "Manning, C D", "Finn, C", "Modarressi, A", "Fayyaz, M", "Yaghoobzadeh, Y", "Pilehvar, M T", "Modarressi, A", "Fayyaz, M", "Aghazadeh, E", "Yaghoobzadeh, Y", "Pilehvar, M T", "Mohebbi, H", "Zuidema, W", "Chrupała, G", "Alishahi, A", "Molina, R", "Nanda, N", "Chan, L", "Lieberum, T", "Smith, J", "Steinhardt, J", "Nanda, N", "Lee, A", "Wattenberg, M", "Nguyen, A", "Dosovitskiy, A", "Yosinski, J", "Brox, T", "Clune, J", "Nogueira, R", "Jiang, Z", "Lin, J", "Oh, B.-D", "Schuler, W", "Olah, C", "Olah, C", "Olah, C", "Cammarata, N", "Schubert, L", "Goh, G", "Petrov, M", "Carter, S", "Olshausen, B A", "Field, D J", "Ortu, F", "Jin, Z", "Doimo, D", "Sachan, M", "Cazzaniga, A", "Schölkopf, B", "Pal, K", "Sun, J", "Yuan, A", "Wallace, B", "Bau, D", "Park, K", "Choe, Y J", "Veitch, V", "Park, S M", "Georgiev, K", "Ilyas, A", "Leclerc, G", "Ądry, A M", "Pearl, J", "Peters, M E", "Neumann, M", "Zettlemoyer, L", "Yih, W.-T", "Pezeshkpour, P", "Jain, S", "Singh, S", "Wallace, B", "Pimentel, T", "Valvoda, J", "Maudslay, R H", "Zmigrod, R", "Williams, A", "Cotterell, R", "Prakash, N", "Shaham, T R", "Haklay, T", "Belinkov, Y", "Bau, D", "Puccetti, G", "Rogers, A", "Drozd, A", "Dell'orletta, F", "Qi, J", "Fernández, R", "Bisazza, A", "Radford, A", "Jozefowicz, R", "Sutskever, I", "Radford, A", "Narasimhan, K", "Salimans, T", "Sutskever, I", "Radford, A", "Wu, J", "Child, R", "Luan, D", "Amodei, D", "Sutskever, I", "Rajamanoharan, S", "Conmy, A", "Smith, L", "Lieberum, T", "Varma, V", "Kramár, J", "Shah, R", "Nanda, N", "Rajamanoharan, S", "Lieberum, T", "Sonnerat, N", "Conmy, A", "Varma, V", "Kramár, J", "Nanda, N", "Ravfogel, S", "Elazar, Y", "Gonen, H", "Twiton, M", "Goldberg, Y", "Ravfogel, S", "Twiton, M", "Goldberg, Y", "Cotterell, R D", "Ribeiro, M T", "Singh, S", "Guestrin, C", "Rogers, A", "Kovaleva, O", "Rumshisky, A", "Rudman, W", "Chen, C", "Eickhoff, C", "Räuker, T", "Ho, A", "Casper, S", "Hadfield-Menell, D", "Sanyal, S", "Ren, X", "Sarti, G", "Feldhus, N", "Sickert, L", "Van Der Wal, O", "Nissim, M", "Bisazza, A", "Sarti, G", "Chrupała, G", "Nissim, M", "Bisazza, A", "Shah, H", "Ilyas, A", "Madry, A", "Shaham, T R", "Schwettmann, S", "Wang, F", "Rajaram, A", "Hernandez, E", "Andreas, J", "Torralba, A", "Shapley, L S", "Sharma, P", "Ash, J T", "Misra, D", "Shazeer, N", "Shrikumar, A", "Greenside, P", "Kundaje, A", "Simonyan, K", "Vedaldi, A", "Zisserman, A", "Singh, S", "Ravfogel, S", "Herzig, J", "Aharoni, R", "Cotterell, R", "Kumaraguru, P", "Sixt, L", "Granz, M", "Landgraf, T", "Stolfo, A", "Belinkov, Y", "Sachan, M", "Stolfo, A", "Belinkov, Y", "Sachan, M", "Stolfo, A", "Wu, B", "Gurnee, W", "Belinkov, Y", "Song, X", "Sachan, M", "Nanda, N", "Suau, X", "Zappella, L", "Apostoloff, N", "Sundararajan, M", "Taly, A", "Yan, Q", "Syed, A", "Rager, C", "Conmy, A", "Takase, S", "Kiyono, S", "Kobayashi, S", "Suzuki, J", "Templeton, A", "Conerly, T", "Marcus, J", "Henighan, T", "Golubeva, A", "Bricken, T", "Tenney, I", "Das, D", "Pavlick, E", "Tenney, I", "Xia, P", "Chen, B", "Wang, A", "Poliak, A", "Mccoy, R T", "Kim, N", "Durme, B V", "Bowman, S", "Das, D", "Pavlick, E", "Tenney, I", "Wexler, J", "Bastings, J", "Bolukbasi, T", "Coenen, A", "Gehrmann, S", "Jiang, E", "Pushkarna, M", "Radebaugh, C", "Reif, E", "Yuan, A", "Tenney, I", "Mullins, R", "Du, B", "Pandya, S", "Kahng, M", "Dixon, L", "Tian, Y", "Wang, Y", "Zhang, Z", "Chen, B", "Du, S S", "Tibshirani, R", "Tigges, C", "Hollinsworth, O J", "Geiger, A", "Nanda, N", "Timkey, W", "Van Schijndel, M", "Todd, E", "Li, M", "Sharma, A S", "Mueller, A", "Wallace, B C", "Bau, D", "Touvron, H", "Martin, L", "Stone, K", "Albert, P", "Almahairi, A", "Babaei, Y", "Bashlykov, N", "Batra, S", "Bhargava, P", "Bhosale, S", "Bikel, D", "Blecher, L", "Ferrer, C C", "Chen, M", "Cucurull, G", "Esiobu, D", "Fernandes, J", "Fu, J", "Fu, W", "Fuller, B", "Gao, C", "Goswami, V", "Goyal, N", "Hartshorn, A", "Hosseini, S", "Hou, R", "Inan, H", "Kardas, M", "Kerkez, V", "Khabsa, M", "Kloumann, I", "Korenev, A", "Koura, P S", "Lachaux, M.-A", "Lavril, T", "Lee, J", "Liskovich, D", "Lu, Y", "Mao, Y", "Martinet, X", "Mihaylov, T", "Mishra, P", "Molybog, I", "Nie, Y", "Poulton, A", "Reizenstein, J", "Rungta, R", "Saladi, K", "Schelten, A", "Silva, R", "Smith, E M", "Subramanian, R", "Tan, X E", "Tang, B", "Taylor, R", "Williams, A", "Kuan, J X", "Xu, P", "Yan, Z", "Zarov, I", "Zhang, Y", "Fan, A", "Kambadur, M", "Narang, S", "Rodriguez, A", "Stojnic, R", "Edunov, S", "Scialom, T", "Tufanov, I", "Hambardzumyan, K", "Ferrando, J", "Voita, E", "Vasconcelos, H", "Jörke, M", "Grunde-Mclaughlin, M", "Gerstenberg, T", "Bernstein, M S", "Krishna, R", "Vaswani, A", "Shazeer, N", "Parmar, N", "Uszkoreit, J", "Jones, L", "Gomez, A N", "Kaiser, L U", "Polosukhin, I", "Veit, A", "Wilber, M", "Belongie, S", "Vig, J", "Vig, J", "Belinkov, Y", "Vig, J", "Gehrmann, S", "Belinkov, Y", "Qian, S", "Nevo, D", "Singer, Y", "Shieber, S", "Voita, E", "Titov, I", "Voita, E", "Sennrich, R", "Titov, I", "Voita, E", "Talbot, D", "Moiseev, F", "Sennrich, R", "Titov, I", "Voita, E", "Sennrich, R", "Titov, I", "Von Oswald, J", "Niklasson, E", "Randazzo, E", "Sacramento, J", "Mordvintsev, A", "Zhmoginov, A", "Vladymyrov, M", "Wang, K R", "Variengien, A", "Conmy, A", "Shlegeris, B", "Steinhardt, J", "Wang, X", "Wen, K", "Zhang, Z", "Hou, L", "Liu, Z", "Li, J", "Wei, D", "Nair, R", "Dhurandhar, A", "Varshney, K R", "Daly, E", "Singh, M", "Weiss, G", "Goldberg, Y", "Yahav, E", "Wen, K", "Li, Y", "Liu, B", "Risteski, A", "Wolf, T", "Debut, L", "Sanh, V", "Chaumond, J", "Delangue, C", "Moi, A", "Cistac, P", "Rault, T", "Louf, R", "Funtowicz, M", "Davison, J", "Shleifer, S", "Von Platen, P", "Ma, C", "Jernite, Y", "Plu, J", "Xu, C", "Scao, T Le", "Gugger, S", "Drame, M", "Lhoest, Q", "Rush, A", "Wright, B", "Sharkey, L", "Wu, W", "Wang, Y", "Xiao, G", "Peng, H", "Fu, Y", "Wu, Z", "D'oosterlinck, K", "Geiger, A", "Zur, A", "Potts, C", "Wu, A", "Geiger, T", "Icard, C", "Potts, N", "Goodman", "Xiao, G", "Tian, Y", "Chen, B", "Han, S", "Lewis, M", "Xie, S M", "Raghunathan, A", "Liang, P", "Ma, T", "Xiong, R", "Yang, Y", "He, D", "Zheng, K", "Zheng, S", "Xing, C", "Zhang, H", "Lan, Y", "Wang, L", "Liu, T.-Y", "Yang, S", "Huang, S", "Zou, W", "Zhang, J", "Dai, X", "Chen, J", "Yao, Y", "Wang, P", "Tian, B", "Cheng, S", "Li, Z", "Deng, S", "Chen, H", "Zhang, N", "Yin, K", "Neubig, G", "Yu, J", "Merullo, E", "Pavlick", "Yu, Y", "Buchanan, S", "Pai, D", "Chu, T", "Wu, Z", "Tong, S", "Haeffele, B D", "Ma, Y", "Yuksekgonul, M", "Chandrasekaran, V", "Jones, E", "Gunasekar, S", "Naik, R", "Palangi, H", "Kamar, E", "Nushi, B", "Zeiler, M D", "Fergus, R", "Zhang, B", "Sennrich, R", "Zhang, F", "Nanda, N", "Zheng, C", "Yin, F", "Zhou, H", "Meng, F", "Zhou, J", "Chang, K.-W", "Huang, M", "Peng, N", "Zhong, Z", "Liu, Z", "Tegmark, M", "Andreas, J", "Zhou, B", "Khosla, A", "Lapedriza, A", "Oliva, A", "Torralba, A", "Zhou, H", "Bradley, A", "Littwin, E", "Razin, N", "Saremi, O", "Susskind, J M", "Bengio, S", "Nakkiran, P", "Zou, A", "Phan, L", "Chen, S", "Campbell, J", "Guo, P", "Ren, R", "Pan, A", "Yin, X", "Mazeika, M", "Dombrowski, A.-K", "Goel, S", "Li, N", "Byun, M J", "Wang, Z", "Mallen, A", "Basart, S", "Koyejo, S", "Song, D", "Fredrikson, M", "Kolter, J Z", "Hendrycks ; Conerly, D"]
year: 2024
venue: "Arxiv"
doi: "10.18653/v1/2020.acl-main.385"
arxiv: "2405.00208"
type: "paper"
status: "unread"
added: "2026-02-26"
---

# A Primer On The Inner Workings Of Transformer-Based Language Models

**Ferrando, Javier et al.** • 2024

> [!quote] Memorable Quote
> ""

## Quick Refresh



## Why You Cared



## Key Concepts



## Cites (Key Papers)

- [[Abnar S. & Zuidema W. (2020) - Quantifying attention flow in transformers]]
- [[Achtibat R., Hatefi S. M., Dreyer M., Jain A., Wiegand T., Lapuschkin S. & Samek W. (2024) - AttnLRP: Attention-aware layer-wise relevance propagation fo...]]
- [[Adebayo J., Gilmer J., Muelly M., Goodfellow I., Hardt M. & Kim B. (2018) - Sanity checks for saliency maps]]
- [[Adebayo J., Muelly M., Liccardi I. & Kim B. (2020) - Debugging tests for model explanations]]
- [[Adebayo J., Muelly M., Abelson H. & Kim B. (2022) - Post hoc explanations may be ineffective for detecting unkno...]]
- [[Agarwal C., Tanneru S. H. & Lakkaraju H. (2024) - Faithfulness vs. plausibility: On the (un)reliability of exp...]]
- [[Ahmadian A., Dash S., Chen H., Venkitesh B., Gou Z. S., Blunsom P., Üstün A. & Hooker S. (2023) - Intriguing properties of quantization at scale]]
- [[Akyurek E., Bolukbasi T., Liu F., Xiong B., Tenney I., Andreas J. & Guu K. (2022) - Towards tracing knowledge in language models back to the tra...]]
- [[Akyürek E., Schuurmans D., Andreas J., Ma T. & Zhou D. (2023) - What learning algorithm is in-context learning? investigatio...]]
- [[Akyürek E., Wang B., Kim Y. & Andreas J. (2024) - In-context language learning: Architectures and algorithms]]

*(426 more citations below)*

## Cited By

*This section will be populated as you process papers that cite this one.*

## Details

**Published:** Arxiv
**DOI:** [10.18653/v1/2020.acl-main.385](https://doi.org/10.18653/v1/2020.acl-main.385)
**arXiv:** [2405.00208](https://arxiv.org/abs/2405.00208)
**PDF:** [[arxiv_2405.00208.pdf]]

## Abstract

The rapid progress of research aimed at interpreting the inner workings of advanced language models has highlighted a need for contextualizing the insights gained from years of work in this area. This primer provides a concise technical introduction to the current techniques used to interpret the inner workings of Transformer-based language models, focusing on the generative decoder-only architecture. We conclude by presenting a comprehensive overview of the known internal mechanisms implemented by these models, uncovering connections across popular approaches and active research directions in this area.

## Full Citation List

1. Abnar S. & Zuidema W. (2020). Quantifying attention flow in transformers. DOI: 10.18653/v1/2020.acl-main.385
2. Achtibat R., Hatefi S. M., Dreyer M. et al. (2024). AttnLRP: Attention-aware layer-wise relevance propagation for transformers.
3. Adebayo J., Gilmer J., Muelly M. et al. (2018). Sanity checks for saliency maps.
4. Adebayo J., Muelly M., Liccardi I. et al. (2020). Debugging tests for model explanations.
5. Adebayo J., Muelly M., Abelson H. et al. (2022). Post hoc explanations may be ineffective for detecting unknown spurious correlation.
6. Agarwal C., Tanneru S. H. & Lakkaraju H. (2024). Faithfulness vs. plausibility: On the (un)reliability of explanations from large language models.
7. Ahmadian A., Dash S., Chen H. et al. (2023). Intriguing properties of quantization at scale.
8. Akyurek E., Bolukbasi T., Liu F. et al. (2022). Towards tracing knowledge in language models back to the training data. DOI: 10.18653/v1/2022.findings-emnlp.180
9. Akyürek E., Schuurmans D., Andreas J. et al. (2023). What learning algorithm is in-context learning? investigations with linear models.
10. Akyürek E., Wang B., Kim Y. et al. (2024). In-context language learning: Architectures and algorithms.
11. Alain G. & Bengio Y. (2016). Understanding intermediate layers using linear classifier probes. Arxiv, pp. 13.
12. Alammar J. (2021). Ecco: An open source library for the explainability of transformer language models. DOI: 10.18653/v1/2021.acl-demo.30
13. Ali A., Schnake T., Eberle O. et al. (2022). XAI for transformers: Better explanations through conservative propagation.
14. Ali A., Zimerman I. & Wolf L. (2024). The hidden attention of mamba models.
15. Amara K., Sevastjanova R. & El-Assady M. (2024). Syntaxshap: Syntax-aware explainability method for text generation.
16. Anil C., Wu Y., Andreassen A. J. et al. (2022). Exploring length generalization in large language models.
17. Anthropic (2024). Introducing the next generation of claude.
18. Arditi A., Obeso O., Syed A. et al. (2024). Refusal in language models is mediated by a single direction. Arxiv, pp. 15.
19. Arora A., Jurafsky D. & Potts C. (2024). Causalgym: Benchmarking causal interpretability methods on linguistic tasks.
20. Arora S., Li Y., Liang Y. et al. (2018). Linear algebraic structure of word senses, with applications to polysemy. Transactions of the Association for Computational Linguistics, Vol. 6, pp. 15. DOI: 10.1162/tacl_a_00034
21. Atanasova P., Simonsen J. G., Lioma C. et al. (2020). A diagnostic study of explainability techniques for text classification. DOI: 10.18653/v1/2020.emnlp-main.263
22. Atanasova P., Camburu O., Lioma C. et al. (2023). Faithfulness tests for natural language explanations. DOI: 10.18653/v1/2023.acl-short.25
23. Attanasio G., Pastor E., Bonaventura C. D. et al. (2023). ferret: a framework for benchmarking explainers on transformers. DOI: 10.18653/v1/2023.eacl-demo.29
24. Avitan M., Cotterell R., Goldberg Y. et al. (2024). What changed? converting representational interventions to natural language. Arxiv, pp. 32.
25. Azaria A. & Mitchell T. (2023). The internal state of an LLM knows when it's lying. DOI: 10.18653/v1/2023.findings-emnlp.68
26. Ba J. L., Kiros J. R. & Hinton G. E. (2016). Layer normalization. Arxiv, pp. 3.
27. On pixel-wise explanations for non-linear classifier decisions by layer-wise relevance propagation SBach ABinder GMontavon FKlauschen K.-RMüller WSamek 10.1371/journal.pone.0130140 PLOS ONE 10 7 7
28. Bai Y., Jones A., Ndousse K. et al. (2022). Training a helpful and harmless assistant with reinforcement learning from human feedback. ArXiv, pp. 15.
29. Balduzzi D., Frean M., Leary L. et al. (2017). The shattered gradients problem: If resnets are the answer, then what is the question?.
30. Bastings J. & Filippova K. (2020). The elephant in the interpretability room: Why use attention as explanation when we have saliency methods?. DOI: 10.18653/v1/2020.blackboxnlp-1.14
31. Bastings J., Ebert S., Zablotskaia P. et al. (2022). will you find these shortcuts?" a protocol for evaluating the faithfulness of input salience methods for text classification. DOI: 10.18653/v1/2022.emnlp-main.64
32. Bau A., Belinkov Y., Sajjad H. et al. (2019). Identifying and controlling important neurons in neural machine translation.
33. Bau D., Zhu J., Strobelt H. et al. (2020). Understanding the role of individual units in a deep neural network. Proceedings of the National Academy of Sciences, Vol. 117(48), pp. 14. DOI: 10.1073/pnas.1907375117
34. Bau D., Wallace B. C., Guha A. et al. (2023). National deep inference facility for very large language models (ndif).
35. Belinkov Y. (2022). Probing classifiers: Promises, shortcomings, and advances. Computational Linguistics, Vol. 48(1), pp. 207-219. DOI: 10.1162/coli_a_00422
36. Belinkov Y. & Glass J. (2019). Analysis methods in neural language processing: A survey. Transactions of the Association for Computational Linguistics, Vol. 7, pp. 14. DOI: 10.1162/tacl_a_00254
37. Belinkov Y., Durrani N., Dalvi F. et al. (2017). What do neural machine translation models learn about morphology?. DOI: 10.18653/v1/P17-1080
38. Belrose N. (2023). Least-squares concept erasure with oracle concept labels.
39. Belrose N. (2024). Sparse autoencoders. GitHub repository.
40. Belrose N., Furman Z., Smith L. et al. (2023). Eliciting latent predictions from transformers with the tuned lens. Arxiv, pp. 31.
41. LEACE: Perfect linear concept erasure in closed form NBelrose DSchneider-Joseph SRavfogel RCotterell ERaff SBiderman Thirty-seventh Conference on Neural Information Processing Systems, 2023b 14
42. Bengio Y., Ducharme R., Vincent P. et al. (2003). A neural probabilistic language model. J. Mach. Learn. Res, Vol. 3, pp. 2.
43. Bereska L. & Gavves E. (2024). Mechanistic interpretability for ai safety -a review. ArXiv, pp. 2.
44. Berglund L., Tong M., Kaufmann M. et al. (2023). The reversal curse: Llms trained on "a is b" fail to learn "b is a.
45. Bibal A., Cardon R., Alfter D. et al. (2022). Is attention explanation? an introduction to the debate. DOI: 10.18653/v1/2022.acl-long.269
46. Pythia: a suite for analyzing large language models across training and scaling SBiderman HSchoelkopf QAnthony HBradley KO'brien EHallahan MAKhan SPurohit USPrashanth ERaff ASkowron LSutawika OVan Der Wal Proceedings of the 40th International Conference on Machine Learning, ICML'23 the 40th International Conference on Machine Learning, ICML'23 21
47. Bietti A., Cabannes V., Bouchacourt D. et al. (2023). Birth of a transformer: A memory viewpoint.
48. Language models can explain neurons in language models SBills NCammarata DMossing HTillman LGao GGoh ISutskever JLeike JWu WSaunders 32 19
49. Bilodeau B., Jaques N., Koh P. W. et al. (2024). Impossibility theorems for feature attribution. Proceedings of the National Academy of Sciences, Vol. 121(2), pp. 8. DOI: 10.1073/pnas.2304406120
50. Bloom J. (2024). Open source sparse autoencoders for all residual stream layers of GPT2 small. AI Alignment Forum.
51. Bloom J. & Channin D. (2024). Saelens. GitHub repository.
52. Bloom J. & Lin J. (2024). Understanding SAE features with the logit lens.
53. An interpretability illusion for bert TBolukbasi APearce AYuan ACoenen EReif FViégas MWattenberg 19
54. Bondarenko Y., Nagel M. & Blankevoort T. (2023). Quantizable transformers: Removing outliers by helping attention heads do nothing.
55. Bricken T., Templeton A., Batson J. et al. (2023). Towards monosemanticity: Decomposing language models with dictionary learning.
56. Brody S., Alon U. & Yahav E. (2023). On the expressivity role of LayerNorm in transformers' attention. DOI: 10.18653/v1/2023.findings-acl.895
57. Brown D., Vyas N. & Bansal Y. (2023). On privileged and convergent bases in neural network representations.
58. Brown T., Mann B., Ryder N. et al. (2020). Language models are few-shot learners.
59. Brunet M., Alkalay-Houlihan C., Anderson A. et al. (2019). Understanding the origins of bias in word embeddings.
60. Brunner G., Liu Y., Pascual D. et al. (2020). On identifiability in transformers.
61. Burns C., Ye H., Klein D. et al. (2023). Discovering latent knowledge in language models without supervision.
62. Bussmann B., Leask P. & Nanda N. (2024). Batchtopk: A simple improvement for topk-saes. AI Alignment Forum.
63. NCammarata SCarter GGoh COlah MPetrov LSchubert CVoss BEgan SKLim 10.23915/distill.00024 11 Thread: Circuits. Distill, 2020
64. Cancedda N. (2024). Spectral filters, dark signals, and attention sinks.
65. Casper S., Ezell C., Siegmann C. et al. (2024). Black-box access is insufficient for rigorous ai audits.
66. Ch-Wang S., Durme B. V., Eisner J. et al. (2023). Do androids know they're only dreaming of electric sheep?.
67. Chan L., Garriga-Alonso A., Goldwosky-Dill N. et al. (2022). Causal scrubbing, a method for rigorously testing interpretability hypotheses. AI Alignment Forum.
68. Chefer H., Gur S. & Wolf L. (2021). Transformer interpretability beyond attention visualization.
69. Sudden drops in the loss: Syntax acquisition, phase transitions, and simplicity bias in MLMs AChen RShwartz-Ziv KCho MLLeavitt NSaphra The Twelfth International Conference on Learning Representations, 2024a 20
70. INSIDE: LLMs' internal states retain the power of hallucination detection CChen KLiu ZChen YGu YWu MTao ZFu JYe The Twelfth International Conference on Learning Representations, 2024b 27
71. Chen H., Vondrick C. & Mao C. (2024). Selfie: Self-interpretation of large language model embeddings.
72. Chen S., Xiong M., Liu J. et al. (2024). In-context sharpness as alerts: An inner representation perspective for hallucination mitigation.
73. Chowdhery A., Narang S., Devlin J. et al. (2023). Palm: Scaling language modeling with pathways. Journal of Machine Learning Research, Vol. 24(240), pp. 1-113.
74. Chowdhury A. G., Islam M. M., Kumar V. et al. (2024). Breaking down the defenses: A comparative survey of attacks on large language models.
75. Chuang Y., Xie Y., Luo H. et al. (2024). Dola: Decoding by contrasting layers improves factuality in large language models.
76. Chughtai B., Cooney A. & Nanda N. (2024). Summing up the facts: Additive mechanisms behind factual recall in llms.
77. Clark K., Khandelwal U., Levy O. et al. (2019). What does BERT look at? an analysis of BERT's attention. DOI: 10.18653/v1/W19-4828
78. Conerly T., Templeton A., Bricken T. et al. (2024). Circuits updates -april 2024. update on how we train saes.
79. Conmy A., Mavor-Parker A., Lynch A. et al. (2023). Towards automated circuit discovery for mechanistic interpretability.
80. ACooney Circuitvis December 2022 31
81. Cooney A. (2023). Sparse autoencoder. GitHub repository.
82. Correia G. M., Niculae V. & Martins A. F. (2019). Adaptively sparse transformers. DOI: 10.18653/v1/D19-1223
83. Costa-Jussà M., Smith E., Ropers C. et al. (2023). Toxicity in multilingual machine translation at scale. DOI: 10.18653/v1/2023.findings-emnlp.642
84. Covert I., Lundberg S. & Lee S. (2021). Explaining by removing: A unified framework for model explanation. Journal of Machine Learning Research, Vol. 22(209), pp. 7.
85. Crabbé J. & Van Der Schaar M. (2023). Evaluating the robustness of interpretability methods through explanation invariance and equivariance.
86. Csordás R., Van Steenkiste S. & Schmidhuber J. (2021). Are neural nets modular? inspecting functional modularity through differentiable weight masks.
87. Cunningham H., Ewart A., Riggs L. et al. (2023). Sparse autoencoders find highly interpretable features in language models. Arxiv, pp. 25.
88. Dai D., Dong L., Hao Y. et al. (2022). Knowledge neurons in pretrained transformers. DOI: 10.18653/v1/2022.acl-long.581
89. Dale D., Voita E., Barrault L. et al. (2023). Detecting and mitigating hallucinations in machine translation: Model internal workings alone do well, sentence similarity Even better. DOI: 10.18653/v1/2023.acl-long.3
90. Dale D., Voita E., Lam J. et al. (2023). HalOmi: A manually annotated benchmark for multilingual hallucination and omission detection in machine translation. DOI: 10.18653/v1/2023.emnlp-main.42
91. Dalvi F., Durrani N., Sajjad H. et al. (2019). What is one grain of sand in the desert? analyzing individual neurons in deep nlp models. DOI: 10.1609/aaai.v33i01.33016309
92. Daniel Johnson P. A. & Penzai (2024). GitHub repository.
93. Dao J., Lau Y., Rager C. et al. (2023). An adversarial example for direct logit attribution: Memory management in gelu.
94. Dar G., Geva M., Gupta A. et al. (2023). Analyzing transformers in embedding space. DOI: 10.18653/v1/2023.acl-long.893
95. Darcet T., Oquab M., Mairal J. et al. (2024). Vision transformers need registers.
96. Dauphin Y. N., Fan A., Auli M. et al. (2017). Language modeling with gated convolutional networks.
97. De Cao N., Schlichtkrull M. S., Aziz W. et al. (2020). How do decisions emerge across layers in neural models? interpretation with differentiable masking.
98. Editing factual knowledge in language models NDe Cao WAziz ITitov 10.18653/v1/2021.emnlp-main.522 Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing M.-FMoens XHuang LSpecia SW-T Yih the 2021 Conference on Empirical Methods in Natural Language Processing Dominican Republic Association for Computational Linguistics 30 Online and Punta Cana November 2021
99. De Cao N., Schmid L., Hupkes D. et al. (2022). Sparse interventions in language models with differentiable masking. DOI: 10.18653/v1/2022.blackboxnlp-1.2
100. Deiseroth B., Deb M., Weinbach S. et al. (2023). Atman: Understanding transformer predictions through memory efficient attention manipulation.
101. Denil M., Demiraj A. & De Freitas N. (2015). Extraction of salient sentences from labelled documents. Arxiv, pp. 7.
102. Dettmers T., Lewis M., Belkada Y. et al. (2022). 8-bit matrix multiplication for transformers at scale.
103. Devlin J., Chang M., Lee K. et al. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. DOI: 10.18653/v1/N19-1423
104. Deyoung J., Jain S., Rajani N. F. et al. (2020). ERASER: A benchmark to evaluate rationalized NLP models. DOI: 10.18653/v1/2020.acl-main.408
105. Dhamdhere K., Sundararajan M. & Yan Q. (2019). How important is a neuron.
106. Dhanorkar S., Wolf C. T., Qian K. et al. (2021). Who needs to know what, when?: Broadening the explainable ai (xai) design space by looking at explanations across the ai lifecycle. DOI: 10.1145/3461778.3462131
107. Din A. Y., Karidi T., Choshen L. et al. (2023). Jump to conclusions: Short-cutting transformers with linear transformations. Arxiv, pp. 18.
108. Ding S., Koehn P., Toutanova K. et al. (2021). Evaluating saliency methods for neural language models. DOI: 10.18653/v1/2021.naacl-main.399
109. Doshi-Velez F. & Kim B. (2017). Towards a rigorous science of interpretable machine learning.
110. Durrani N., Dalvi F. & Sajjad H. (2023). Discovering salient neurons in deep nlp models. Journal of Machine Learning Research, Vol. 24(362), pp. 23.
111. Elazar Y., Ravfogel S., Jacovi A. et al. (2021). Amnesic probing: Behavioral explanation with amnesic counterfactuals. Transactions of the Association for Computational Linguistics, Vol. 9, pp. 15. DOI: 10.1162/tacl_a_00359
112. A mathematical framework for transformer circuits NElhage NNanda COlsson THenighan NJoseph BMann AAskell YBai AChen TConerly NDassarma DDrain DGanguli ZHatfield-Dodds DHernandez AJones JKernion LLovitt KNdousse DAmodei TBrown JClark JKaplan SMccandlish COlah Transformer Circuits Thread, 2021a p. 2, 3, 6, 20, 21, 24, 25
113. NElhage NNanda COlsson THenighan NJoseph BMann AAskell YBai AChen TConerly NDassarma DDrain DGanguli ZHatfield-Dodds DHernandez AJones JKernion LLovitt KNdousse DAmodei TBrown JClark JKaplan SMccandlish COlah Garcon Transformer Circuits Thread, 2021b 30
114. NElhage THume COlsson NNanda THenighan SJohnston SElshowk NJoseph NDassarma BMann DHernandez AAskell KNdousse AJones DDrain AChen YBai DGanguli LLovitt ZHatfield-Dodds JKernion TConerly SKravec SFort SKadavath JJacobson ETran-Johnson JKaplan JClark TBrown SMccandlish DAmodei COlah Softmax linear units. Transformer Circuits Thread, 2022a 23
115. Elhage N., Hume T., Olsson C. et al. (2022). Toy models of superposition. Transformer Circuits Thread.
116. Elhage N., Lasenby R. & Olah C. (2023). Privileged bases in the transformer residual stream.
117. Enguehard J. (2023). Sequential integrated gradients: a simple but effective method for explaining language models. DOI: 10.18653/v1/2023.findings-acl.477
118. Erichson N. B., Yao Z. & Mahoney M. W. (2019). Jumprelu: A retrofit defense strategy for adversarial attacks. ArXiv, pp. 17.
119. Ethayarajh K. (2019). How contextual are contextualized word representations? Comparing the geometry of BERT, ELMo, and GPT-2 embeddings. DOI: 10.18653/v1/D19-1006
120. Ethayarajh K. & Jurafsky D. (2021). Attention flows are shapley value explanations. DOI: 10.18653/v1/2021.acl-short.8
121. Fantozzi P. & Naldi M. (2024). The explainability of transformers: Current status and directions. Computers, Vol. 13(4), pp. 6. DOI: 10.3390/computers13040092
122. Feldhus N., Hennig L., Nasert M. D. et al. (2023). Saliency map verbalization: Comparing feature importance representations from model-free and instruction-based methods. DOI: 10.18653/v1/2023.nlrse-1.4
123. Ferrando J. & Costa-Jussà M. R. (2021). Attention weights in transformer NMT fail aligning words between sequences but largely explain model predictions. DOI: 10.18653/v1/2021.findings-emnlp.39
124. Ferrando J. & Costa-Jussà M. R. (2024). On the similarity of circuits across languages: a case study on the subjectverb agreement task. arXiv.
125. JFerrando EVoita Information flow routes: Automatically interpreting language models at scale. arXiv, 2024 12, 20, 21, 22 4
126. Ferrando J., Gállego G. I., Alastruey B. et al. (2022). Towards opening the black box of neural machine translation: Source and target interpretations of the transformer. DOI: 10.18653/v1/2022.emnlp-main.599
127. Ferrando J., Gállego G. I. & Costa-Jussà M. R. (2022). Measuring the mixing of contextual information in the transformer. DOI: 10.18653/v1/2022.emnlp-main.595
128. Ferrando J., Gállego G. I., Tsiamas I. et al. (2023). Explaining how transformers use context to build predictions. DOI: 10.18653/v1/2023.acl-long.301
129. Fierro C. & Søgaard A. (2022). Factual consistency of multilingual pretrained language models. DOI: 10.18653/v1/2022.findings-acl.240
130. Fiotto-Kaufman J. (2024). The package for interpreting and manipulating the internals of deep learned models.
131. Fomicheva M., Sun S., Yankovskaya L. et al. (2020). Unsupervised quality estimation for neural machine translation. Transactions of the Association for Computational Linguistics, Vol. 8, pp. 27. DOI: 10.1162/tacl_a_00330
132. Friedman D., Wettig A. & Chen D. (2023). Learning transformer programs.
133. Gao L., Tour T. D., Tillman H. et al. (2024). Scaling and evaluating sparse autoencoders.
134. Geiger A., Richardson K. & Potts C. (2020). Neural natural language inference models partially embed theories of lexical entailment and negation. DOI: 10.18653/v1/2020.blackboxnlp-1.16
135. Geiger A., Lu H., Icard T. et al. (2021). Causal abstractions of neural networks.
136. Geiger A., Wu Z., Lu H. et al. (2022). Inducing causal structure for interpretable neural networks.
137. Geiger A., Potts C. & Icard T. (2023). Causal abstraction for faithful model interpretation.
138. Geiger A., Wu Z., Potts C. et al. (2023). Finding alignments between interpretable causal variables and distributed neural representations.
139. Team G. G., Mesnard T., Hardin C. et al. (2024). Open models based on gemini research and technology.
140. Geva M., Schuster R., Berant J. et al. (2021). Transformer feed-forward layers are key-value memories. DOI: 10.18653/v1/2021.emnlp-main.446
141. Geva M., Caciularu A., Dar G. et al. (2022). LM-debugger: An interactive tool for inspection and intervention in transformer-based language models. DOI: 10.18653/v1/2022.emnlp-demos.2
142. Geva M., Caciularu A., Wang K. et al. (2022). Transformer feed-forward layers build predictions by promoting concepts in the vocabulary space. DOI: 10.18653/v1/2022.emnlp-main.3
143. Geva M., Bastings J., Filippova K. et al. (2023). Dissecting recall of factual associations in autoregressive language models. DOI: 10.18653/v1/2023.emnlp-main.751
144. Ghandeharioun A., Caciularu A., Pearce A. et al. (2024). Patchscopes: A unifying framework for inspecting hidden representations of language models. Arxiv, pp. 18.
145. Goldowsky-Dill N., Macleod C., Sato L. et al. (2023). Localizing model behavior with path patching. Arxiv, pp. 12.
146. Gould R., Ong E., Ogden G. et al. (2024). Successor heads: Recurring, interpretable attention heads in the wild.
147. DGroeneveld IBeltagy PWalsh ABhagia RKinney OTafjord AHJha HIvison IMagnusson YWang SArora DAtkinson RAuthur KRChandu ACohan JDumas YElazar YGu JHessel TKhot WMerrill JMorrison NMuennighoff ANaik CNam MEPeters VPyatkin ARavichander DSchwenk SShah WSmith EStrubell NSubramani MWortsman PDasigi NLambert KRichardson LZettlemoyer JDodge KLo LSoldaini NASmith HHajishirzi 2024 4 Olmo: Accelerating the science of language models
148. Grosse R. B., Bae J., Anil C. et al. (2023). Studying large language model generalization with influence functions.
149. Gu A. & Dao T. (2023). Mamba: Linear-time sequence modeling with selective state spaces.
150. Gu J., Xu H., Ma J. et al. (2024). Model editing can hurt general abilities of large language models.
151. Guerner C., Svete A., Liu T. et al. (2023). A geometric notion of causal probing.
152. Guerreiro N. M., Colombo P., Piantanida P. et al. (2023). Optimal transport for unsupervised hallucination detection in neural machine translation. DOI: 10.18653/v1/2023.acl-long.770
153. Guerreiro N. M., Voita E. & Martins A. (2023). Looking for a needle in a haystack: A comprehensive study of hallucinations in neural machine translation. DOI: 10.18653/v1/2023.eacl-main.75
154. Gupta A., Boleda G., Baroni M. et al. (2015). Distributional vectors encode referential attributes. DOI: 10.18653/v1/D15-1002
155. Gupta A., Rao A. & Anumanchipalli G. K. (2024). Model editing at scale leads to gradual and catastrophic forgetting.
156. Gupta A., Sajnani D. & Anumanchipalli G. (2024). A unified framework for model editing.
157. Gurnee W. (2024). Sae reconstruction errors are (empirically) pathological. AI Alignment Forum.
158. Gurnee W. & Tegmark M. (2024). Language models represent space and time.
159. Gurnee W., Nanda N., Pauly M. et al. (2023). Finding neurons in a haystack: Case studies with sparse probing. Transactions on Machine Learning Research, Vol. 23, pp. 24.
160. Gurnee W., Horsley T., Guo Z. C. et al. (2024). Universal neurons in gpt2 language models.
161. Guu K., Webson A., Pavlick E. et al. (2023). Simfluence: Modeling the influence of individual training examples by simulating training runs. Arxiv, pp. 8.
162. Hammoudeh Z. & Lowd D. (2022). Training data influence analysis and estimation: A survey.
163. Han X., Wallace B. C. & Tsvetkov Y. (2020). Explaining black box predictions and unveiling data artifacts through influence functions. DOI: 10.18653/v1/2020.acl-main.492
164. Han Z., Gao C., Liu J. et al. (2024). Parameter-efficient fine-tuning for large models: A comprehensive survey.
165. Hanna M., Liu O. & Variengien A. (2023). How does GPT-2 compute greater-than?: Interpreting mathematical abilities in a pre-trained language model.
166. Hanna M., Pezzelle S. & Belinkov Y. (2024). Have faith in faithfulness: Going beyond circuit overlap when finding model mechanisms.
167. Hase P., Bansal M., Kim B. et al. (2023). Does localization inform editing? surprising differences in causality-based localization vs. knowledge editing in language models.
168. Haviv A., Cohen I., Gidron J. et al. (2023). Understanding transformer memorization recall through idioms. DOI: 10.18653/v1/2023.eacl-main.19
169. He Z., Ge X., Tang Q. et al. (2024). Dictionary learning improves patch-free circuit discovery in mechanistic interpretability: A case study on othello-gpt.
170. Heimersheim S. & Janiak J. (2023). A circuit for python docstrings in a 4-layer attention-only transformer.
171. Heimersheim S. & Nanda N. (2024). How to use and interpret activation patching. Arxiv, pp. 10.
172. Heimersheim S. & Turner A. (2023). Residual stream norms grow exponentially over the forward pass.
173. Hendel R., Geva M. & Globerson A. (2023). In-context learning creates task vectors. Arxiv, Vol. 26, pp. 25.
174. Hernandez E., Sharma A. S., Haklay T. et al. (2024). Linearity of relation decoding in transformer language models.
175. Hewitt J. & Liang P. (2019). Designing and interpreting probes with control tasks. DOI: 10.18653/v1/D19-1275
176. Hewitt J. & Manning C. D. (2019). A structural probe for finding syntax in word representations. DOI: 10.18653/v1/N19-1419
177. Hewitt J., Thickstun J., Manning C. et al. (2023). Backpack language models. DOI: 10.18653/v1/2023.acl-long.506
178. Himmi A., Staerman G., Picot M. et al. (2024). Enhanced hallucination detection in neural machine translation through simple detector aggregation.
179. Hoffmann J., Borgeaud S., Mensch A. et al. (2022). An empirical analysis of computeoptimal large language model training.
180. Holtzman A., West P., Shwartz V. et al. (2021). Surface form competition: Why the highest probability answer isn't always right. DOI: 10.18653/v1/2021.emnlp-main.564
181. Hoover B., Strobelt H. & Gehrmann S. (2020). exBERT: A Visual Analysis Tool to Explore Learned Representations in Transformer Models. DOI: 10.18653/v1/2020.acl-demos.22
182. Htut P. M., Phang J., Bordia S. et al. (2019). Do attention heads in bert track syntactic dependencies? Arxiv.
183. Hu P., Chang R., Luo H. et al. (2024). Outlier-efficient hopfield layers for large transformer-based models.
184. Huang J., Geiger A., D'oosterlinck K. et al. (2023). Rigorously assessing natural language explanations of neurons. DOI: 10.18653/v1/2023.blackboxnlp-1.24
185. JHuang ZWu CPotts MGeva AGeiger Ravel Evaluating interpretability methods on disentangling language model representations, 2024a 15
186. Huang Y., Hu S., Han X. et al. (2024). Unified view of grokking, double descent and emergent abilities: A perspective from circuits competition.
187. Hudson N., Pauloski J. G., Baughman M. et al. (2024). Trillion parameter ai serving infrastructure for scientific discovery: A survey and vision. Arxiv, pp. 32.
188. Hupkes D., Veldhoen S. & Zuidema W. (2018). Visualisation and 'diagnostic classifiers' reveal how recurrent and recursive neural networks process hierarchical structure. Journal of Artificial Intelligence Research, Vol. 61(1), pp. 14.
189. Jain S., Kirk R., Lubana E. S. et al. (2024). What happens when you fine-tuning your model? mechanistic analysis of procedurally generated tasks.
190. Jain S. & Wallace B. C. (2019). Attention is not Explanation. DOI: 10.18653/v1/N19-1357
191. Jastrzębski S., Arpit D., Ballas N. et al. (2018). Residual connections encourage iterative inference.
192. Jeffrey Wu T. D. & Gao L. (2024). Sparse autoencoders. GitHub repository.
193. Jermyn A. & Templeton A. (2024). Circuits updates -jnauary 2024. ghost grads: An improvement on resampling.
194. Ji Z., Lee N., Frieske R. et al. (2023). Survey of hallucination in natural language generation. ACM Computing Surveys, Vol. 55(12), pp. 27. DOI: 10.1145/3571730
195. Jiang Y., Rajendran G., Ravikumar P. et al. (2024). On the origins of linear representations in large language models.
196. Joseph S. (2023). Vit prisma: A mechanistic interpretability library for vision transformers.
197. Kamradt G. (2023). Needle in a haystack -pressure testing llms.
198. Kaplan J., Mccandlish S., Henighan T. et al. (2020). Scaling laws for neural language models.
199. Karvonen A., Wright B., Rager C. et al. (2024). Measuring progress in dictionary learning for language model interpretability with board game models.
200. Katz S. & Belinkov Y. (2023). VISIT: Visualizing and interpreting the semantic information flow of transformers. DOI: 10.18653/v1/2023.findings-emnlp.939
201. Katz S., Belinkov Y., Geva M. et al. (2024). Backward lens: Projecting language model gradients into the vocabulary space.
202. Kim B., Wattenberg M., Gilmer J. et al. (2018). Interpretability beyond feature attribution: Quantitative testing with concept activation vectors (TCAV).
203. Kissane C., Krzyzanowski R., Conmy A. et al. (2024). Sparse autoencoders work on attention layer outputs. AI Alignment Forum.
204. Kissane C., Krzyzanowski R., Conmy A. et al. (2024). Attention saes scale to gpt-2 small. AI Alignment Forum.
205. Kobayashi G., Kuribayashi T., Yokoi S. et al. (2020). Attention is not only a weight: Analyzing transformers with vector norms. DOI: 10.18653/v1/2020.emnlp-main.574
206. Kobayashi G., Kuribayashi T., Yokoi S. et al. (2021). Incorporating Residual and Normalization Layers into Analysis of Masked Language Models. DOI: 10.18653/v1/2021.emnlp-main.373
207. Kobayashi G., Kuribayashi T., Yokoi S. et al. (2023). Transformer language models handle word frequency in prediction head. DOI: 10.18653/v1/2023.findings-acl.276
208. Kobayashi G., Kuribayashi T., Yokoi S. et al. (2024). Analyzing feed-forward blocks in transformers through the lens of attention map.
209. Koh P. W. & Liang P. (2017). Understanding black-box predictions via influence functions.
210. Köhn A. (2015). What's in an embedding? analyzing word embeddings through multilingual evaluation. DOI: 10.18653/v1/D15-1246
211. Kokhlikyan N., Miglani V., Martin M. et al. (2020). Captum: A unified and generic model interpretability library for pytorch. Arxiv, pp. 30.
212. Kovaleva A., Romanov A., Rogers A. et al. (2019). Revealing the dark secrets of BERT. DOI: 10.18653/v1/D19-1445
213. Kovaleva S., Kulshreshtha A., Rogers A. et al. (2021). BERT busters: Outlier dimensions that disrupt transformers. DOI: 10.18653/v1/2021.findings-acl.300
214. Kramár J., Lieberum T., Shah R. et al. (2024). Atp*: An efficient and scalable method for localizing llm behaviour to components.
215. Krishna S., Han T., Gu A. et al. (2024). The disagreement problem in explainable machine learning: A practitioner's perspective. ArXiv, pp. 8.
216. Krzyzanowski R., Kissane C., Conmy A. et al. (2024). We inspected every head in GPT-2 small using saes so you don't have to. AI Alignment Forum, pp. 22.
217. Kwon Y., Wu E., Wu K. et al. (2024). Datainf: Efficiently estimating data influence in loRA-tuned LLMs and diffusion models.
218. Lal V., Ma A., Aflalo E. et al. (2021). InterpreT: An interactive visualization tool for interpreting transformers. DOI: 10.18653/v1/2021.eacl-demos.17
219. Langedijk A., Mohebbi H., Sarti G. et al. (2023). Decoderlens: Layerwise interpretation of encoder-decoder transformers.
220. Lanham T., Chen A., Radhakrishnan A. et al. (2023). Measuring faithfulness in chain-ofthought reasoning.
221. Leino K., Sen S., Datta A. et al. (2018). Influence-directed explanations for deep convolutional networks. DOI: 10.1109/TEST.2018.8624792
222. Lepori M. A., Serre T. & Pavlick E. (2023). Uncovering intermediate variables in transformers using circuit probing.
223. Li J., Chen X., Hovy E. et al. (2016). Visualizing and understanding neural models in NLP. DOI: 10.18653/v1/N16-1082
224. Li J., Monroe W. & Jurafsky D. (2017). Understanding neural networks through representation erasure.
225. Inference-time intervention: Eliciting truthful answers from a language model KLi OPatel FViégas HPfister MWattenberg Thirty-seventh Conference on Neural Information Processing Systems, 2023a 27
226. Li X. L., Holtzman A., Fried D. et al. (2023). Contrastive decoding: Open-ended text generation as optimization. DOI: 10.18653/v1/2023.acl-long.687
227. Li Z., Zhang N., Yao Y. et al. (2024). Unveiling the pitfalls of knowledge editing for large language models.
228. Liao V., Gruen D. & Miller S. (2020). Questioning the ai: Informing design practices for explainable ai user experiences. DOI: 10.1145/3313831.3376590
229. Lieberum T., Rahtz M., Kramár J. et al. (2023). Does circuit analysis interpretability scale? evidence from multiple choice capabilities in chinchilla. Arxiv, pp. 10.
230. TLieberum SRajamanoharan AConmy LSmith NSonnerat VVarma JKramár ADragan RShah NNanda Gemma scope: Open sparse autoencoders everywhere all at once on gemma 2. arXiv, 2024 17
231. Lin J. & Bloom J. (2024). Announcing neuronpedia: Platform for accelerating research into sparse autoencoders. AI Alignment Forum.
232. Lin Y., Tan Y. C. & Frank R. (2019). Open sesame: Getting inside BERT's linguistic knowledge. DOI: 10.18653/v1/W19-4825
233. Lindner D., Kramar J., Farquhar S. et al. (2023). Tracr: Compiled transformers as a laboratory for interpretability.
234. Lipton Z. C. (2018). The mythos of model interpretability: In machine learning, the concept of interpretability is both important and slippery. Queue, Vol. 16(3), pp. 6. DOI: 10.1145/3236386.3241340
235. Liu N. F., Gardner M., Belinkov Y. et al. (2019). Linguistic knowledge and transferability of contextual representations. DOI: 10.18653/v1/N19-1112
236. Liu Q., Chai Y., Wang S. et al. (2024). On training data influence of gpt models. Arxiv, pp. 8.
237. Longo L., Brcic M., Cabitza F. et al. (2024). Explainable artificial intelligence (xai) 2.0: A manifesto of open challenges and interdisciplinary research directions. Information Fusion, Vol. 106, pp. 32. DOI: 10.1016/j.inffus.2024.102301
238. Loog M., Viering T., Mey A. et al. (2020). A brief prehistory of double descent. Proceedings of the National Academy of Sciences, Vol. 117(20), pp. 27. DOI: 10.1073/pnas.2001875117
239. GLopardo FPrecioso DGarreau Attention meets post-hoc interpretability: A mathematical perspective. arXiv, 2024 7
240. Lundberg S. M. & Lee S. (2017). A unified approach to interpreting model predictions.
241. Luo Z., Kulmizev A. & Mao X. (2021). Positional artefacts propagate through masked language model embeddings. DOI: 10.18653/v1/2021.acl-long.413
242. Lv A., Zhang K., Chen Y. et al. (2024). Interpreting key mechanisms of factual recall in transformer-based language models. Computing Research Repository, Vol. 29, pp. 21.
243. Lyu Q., Apidianaki M. & Callison-Burch C. (2024). Towards Faithful Model Explanation in NLP: A Survey. Computational Linguistics. DOI: 10.1162/coli_a_00511
244. MMacdiarmid TMaxwell NSchiefer JMu DKaplan SDuvenaud ABowman ETamkin MPerez CSharma EDenison Hubinger Simple probes can catch sleeper agents. Anthropic, 2024 14
245. Madsen A., Reddy S. & Chandar S. (2022). Post-hoc interpretability for neural nlp: A survey. ACM Computing Surveys, Vol. 55(8). DOI: 10.1145/3546577
246. 10.1145/3546577 2
247. Madsen A., Chandar S. & Reddy S. (2024). Are self-explanations from large language models faithful?.
248. Makelov A., Lange G., Geiger A. et al. (2024). Is this the subspace you are looking for? an interpretability illusion for subspace activation patching.
249. Makelov A., Lange G. & Nanda N. (2024). Towards principled evaluations of sparse autoencoders for interpretability and control.
250. Makhzani A. & Frey B. (2014). k-sparse autoencoders.
251. Marks S. & Mueller A. (2023). Dictionary learning. GitHub repository.
252. Marks S. & Tegmark M. (2023). The geometry of truth: Emergent linear structure in large language model representations of true/false datasets.
253. Marks S., Rager C., Michaud E. J. et al. (2024). Sparse feature circuits: Discovering and editing interpretable causal graphs in language models. Computing Research Repository, Vol. 16, pp. 32.
254. Mccoy T., Pavlick E. & Linzen T. (2019). Right for the wrong reasons: Diagnosing syntactic heuristics in natural language inference. DOI: 10.18653/v1/P19-1334
255. Mcdougall C. (2023). Six (and a half) intuitions for SVD.
256. CMcdougall JBloom Sae-vis: Announcement post. Less Wrong, 2024 31
257. Mcdougall C., Conmy A., Rushing C. et al. (2023). Copy suppression: Comprehensively understanding an attention head. Arxiv, pp. 21.
258. Mcgrath T., Kapishnikov A., Tomašev N. et al. (2022). Acquisition of chess knowledge in alphazero. Proceedings of the National Academy of Sciences, Vol. 119(47), pp. 13. DOI: 10.1073/pnas.2206625119
259. Mcgrath T., Rahtz M., Kramar J. et al. (2023). The hydra effect: Emergent self-repair in language model computations. Arxiv, pp. 9.
260. Meng K., Bau D., Andonian A. et al. (2022). Locating and editing factual associations in GPT.
261. Meng K., Sharma A. S., Andonian A. J. et al. (2023). Mass-editing memory in a transformer.
262. Merrill W., Ramanujan V., Goldberg Y. et al. (2021). Effects of parameter norm growth during transformer training: Inductive bias from gradient descent. DOI: 10.18653/v1/2021.emnlp-main.133
263. Merrill W., Tsilivis N. & Shukla A. (2023). A tale of two circuits: Grokking as competition of sparse and dense subnetworks.
264. Merullo J., Eickhoff C. & Pavlick E. (2023). A mechanism for solving relational tasks in transformer language models.
265. Merullo J., Eickhoff C. & Pavlick E. (2024). Circuit component reuse across tasks in transformer language models.
266. Michel P., Levy O. & Neubig G. (2019). Are sixteen heads really better than one?.
267. Mickus T., Paperno D. & Constant M. (2022). How to dissect a Muppet: The structure of transformer embedding spaces. Transactions of the Association for Computational Linguistics, Vol. 10, pp. 5. DOI: 10.1162/tacl_a_00501
268. Miglani V., Yang A., Markosyan A. et al. (2023). Using captum to explain generative language models. DOI: 10.18653/v1/2023.nlposs-1.19
269. Mikolov T., Sutskever I., Chen K. et al. (2013). Distributed representations of words and phrases and their compositionality.
270. Millidge B. & Black S. (2022). The singular value decompositions of transformer weight matrices are highly interpretable. AI Alignment Forum.
271. Millidge B. & Winsor E. (2023). Basic facts about language model internals. AI Alignment Forum.
272. Minaee S., Mikolov T., Nikzad N. et al. (2024). Large language models: A survey.
273. Fast model editing at scale EMitchell CLin ABosselut CFinn CDManning International Conference on Learning Representations, 2022a 30
274. Mitchell E., Lin C., Bosselut A. et al. (2022). Memory-based model editing at scale.
275. Modarressi A., Fayyaz M., Yaghoobzadeh Y. et al. (2022). GlobEnc: Quantifying global token attribution by incorporating the whole encoder layer in transformers. DOI: 10.18653/v1/2022.naacl-main.19
276. Modarressi A., Fayyaz M., Aghazadeh E. et al. (2023). DecompX: Explaining transformers decisions by propagating token decomposition. DOI: 10.18653/v1/2023.acl-long.149
277. Mohebbi H., Zuidema W., Chrupała G. et al. (2023). Quantifying context mixing in transformers. DOI: 10.18653/v1/2023.eacl-main.245
278. Molina R. (2023). Traveling words: A geometric interpretation of transformers. Arxiv, pp. 18.
279. Monea G., Peyrard M., Josifoski M. et al. (2024). A glitch in the matrix? locating and detecting language model grounding with fakepedia.
280. DMossing SBills HTillman TDupré La Tour NCammarata LGao JAchiam CYeh JLeike JWu WSaunders 2024 31 Transformer debugger
281. NNanda Induction mosaic. Neel Nanda Blog, 2022a 21
282. NNanda Neuroscope: A website for mechanistic interpretability of language models. Website, 2022b 19
283. Nanda N. (2023). Attribution patching: Activation patching at industrial scale.
284. Nanda N. & Bloom J. (2022). Transformerlens. Github Repository.
285. Progress measures for grokking via mechanistic interpretability NNanda LChan TLieberum JSmith JSteinhardt The Eleventh International Conference on Learning Representations, 2023a 27
286. Nanda N., Lee A. & Wattenberg M. (2023). Emergent linear representations in world models of self-supervised sequence models. DOI: 10.18653/v1/2023.blackboxnlp-1.2
287. Nanda N., Rajamanoharan S., Kramár J. et al. (2023). Fact finding: Attempting to reverse-engineer factual recall on the neuron level. AI Alignment Forum.
288. Neo C., Cohen S. B. & Barez F. (2024). Interpreting context look-ups in transformers: Investigating attention-mlp interactions.
289. Nguyen A., Dosovitskiy A., Yosinski J. et al. (2016). Synthesizing the preferred inputs for neurons in neural networks via deep generator networks.
290. Nogueira R., Jiang Z. & Lin J. (2020). Investigating the limitations of transformers with simple arithmetic tasks.
291. Oh B. & Schuler W. (2023). Token-wise decomposition of autoregressive language model hidden states for analyzing model predictions. DOI: 10.18653/v1/2023.acl-long.562
292. Olah C. (2022). Mechanistic interpretability, variables, and the importance of interpretable bases.
293. Olah C. (2023). Distributed representations: Composition & superposition.
294. An overview of early vision in inceptionv1. Distill, 2020a COlah NCammarata LSchubert GGoh MPetrov SCarter 10.23915/distill.00024.002 23
295. Olah C., Cammarata N., Schubert L. et al. (2020). Zoom in: An introduction to circuits. Distill, pp. 23. DOI: 10.23915/distill.00024.001
296. Olshausen B. A. & Field D. J. (1997). Sparse coding with an overcomplete basis set: A strategy employed by v1?. Vision Research, Vol. 37(23), pp. 169-176. DOI: 10.1016/S0042-6989(97
297. Olsson C., Elhage N., Nanda N. et al. (2022). -context learning and induction heads. Transformer Circuits Thread.
298. Ortu F., Jin Z., Doimo D. et al. (2024). Competition of mechanisms: Tracing how language models handle facts and counterfactuals. Computing Research Repository, pp. 29.
299. Team G. (2023). Saliency: Framework-agnostic implementation for state-of-the-art saliency methods.
300. Pal K., Sun J., Yuan A. et al. (2023). Future lens: Anticipating subsequent tokens from a single hidden state. DOI: 10.18653/v1/2023.conll-1.37
301. Parcalabescu L. & Frank A. (2023). On measuring faithfulness or self-consistency of natural language explanations.
302. Park K., Choe Y. J. & Veitch V. (2023). The linear representation hypothesis and the geometry of large language models. Arxiv, pp. 14.
303. Trak: attributing model behavior at scale SMPark KGeorgiev AIlyas GLeclerc AMĄdry Proceedings of the 40th International Conference on Machine Learning, ICML'23. JMLR.org, 2023b the 40th International Conference on Machine Learning, ICML'23. JMLR.org, 2023b 8
304. Paulo G., Marshall T. & Belrose N. (2024). Does transformer interpretability transfer to rnns?.
305. Pearl J. (2001). Direct and indirect effects.
306. Pearl J. (2009). Causality. DOI: 10.1017/CBO9780511803161
307. Peters M. E., Neumann M., Zettlemoyer L. et al. (2018). Dissecting contextual word embeddings: Architecture and representation. DOI: 10.18653/v1/D18-1179
308. Pezeshkpour P., Jain S., Singh S. et al. (2022). Combining feature and instance attribution to detect artifacts. DOI: 10.18653/v1/2022.findings-acl.153
309. Pierse C. (2021). Transformers Interpret.
310. Pimentel T., Valvoda J., Maudslay R. H. et al. (2020). Information-theoretic probing for linguistic structure. DOI: 10.18653/v1/2020.acl-main.420
311. Power A., Burda Y., Edwards H. et al. (2022). Grokking: Generalization beyond overfitting on small algorithmic datasets.
312. Prakash N., Shaham T. R., Haklay T. et al. (2024). Fine-tuning enhances existing mechanisms: A case study on entity tracking.
313. Puccetti G., Rogers A., Drozd A. et al. (2022). Outlier dimensions that disrupt transformers are driven by frequency. DOI: 10.18653/v1/2022.findings-emnlp.93
314. Qi J., Fernández R. & Bisazza A. (2023). Cross-lingual consistency of factual knowledge in multilingual language models. DOI: 10.18653/v1/2023.emnlp-main.658
315. Quirke L., Heindrich L., Gurnee W. et al. (2023). Training dynamics of contextual n-grams in language models.
316. Radford A., Jozefowicz R. & Sutskever I. (2017). Learning to generate reviews and discovering sentiment. Arxiv, pp. 14.
317. Radford A., Narasimhan K., Salimans T. et al. (2018). Improving language understanding by generative pre-training.
318. Radford A., Wu J., Child R. et al. (2019). Language models are unsupervised multitask learners.
319. An analysis of encoder representations in transformer-based machine translation ARaganato JTiedemann
320. 10.18653/v1/W18-5431 Proceedings of the 2018 EMNLP Workshop Blackbox NLP: Analyzing and Interpreting Neural Networks for NLP TLinzen GChrupała AAlishahi the 2018 EMNLP Workshop Blackbox NLP: Analyzing and Interpreting Neural Networks for NLPBrussels, Belgium Association for Computational Linguistics November 2018 20
321. Rajamanoharan S. (2024). Progress update 1 from the gdm mech interp team. improving ghost grads. AI Alignment Forum.
322. Rajamanoharan S., Conmy A., Smith L. et al. (2024). Improving dictionary learning with gated sparse autoencoders. ArXiv, Vol. 17, pp. 57.
323. Rajamanoharan S., Lieberum T., Sonnerat N. et al. (2024). Jumping ahead: Improving reconstruction fidelity with jumprelu sparse autoencoders. ArXiv, pp. 17.
324. Ravfogel S., Elazar Y., Gonen H. et al. (2020). Null it out: Guarding protected attributes by iterative nullspace projection. DOI: 10.18653/v1/2020.acl-main.647
325. Ravfogel S., Twiton M., Goldberg Y. et al. (2022). Linear adversarial concept erasure.
326. Ribeiro M. T., Singh S. & Guestrin C. (2016). why should I trust you?": Explaining the predictions of any classifier.
327. Riechers P. M. (2024). Geometry and dynamics of layernorm. arXiv.
328. Rogers A., Kovaleva O. & Rumshisky A. (2021). A Primer in BERTology: What We Know About How BERT Works. Transactions of the Association for Computational Linguistics, Vol. 8, pp. 2-14. DOI: 10.1162/tacl_a_00349
329. Rudman W., Chen C. & Eickhoff C. (2023). Outlier dimensions encode task specific knowledge. DOI: 10.18653/v1/2023.emnlp-main.901
330. Rushing C. & Nanda N. (2024). Explorations of self-repair in language models.
331. Räuker T., Ho A., Casper S. et al. (2023). Toward transparent ai: A survey on interpreting the inner structures of deep neural networks. Arxiv, pp. 2.
332. Sakarvadia M., Khan A., Ajith A. et al. (2023). Attention lens: A tool for mechanistically interpreting the attention head information retrieval mechanism.
333. Sanyal S. & Ren X. (2021). Discretized integrated gradients for explaining language models. DOI: 10.18653/v1/2021.emnlp-main.805
334. Sarti G., Feldhus N., Sickert L. et al. (2023). Inseq: An interpretability toolkit for sequence generation models. DOI: 10.18653/v1/2023.acl-demo.40
335. Sarti G., Chrupała G., Nissim M. et al. (2024). Quantifying the plausibility of context reliance in neural machine translation.
336. Shah H., Ilyas A. & Madry A. (2024). Decomposing and editing predictions by modeling model computation. ArXiv, pp. 10.
337. Shaham T. R., Schwettmann S., Wang F. et al. (2024). A multimodal automated interpretability agent. Arxiv, pp. 31.
338. Shapley L. S. (1953). A value for n-person games.
339. Sharkey L., Braun D. & Millidge B. (2022). Taking features out of superposition with sparse autoencoders. AI Alignment Forum.
340. Sharma A. S., Atkinson D. & Bau D. (2024). Locating and editing factual associations in mamba.
341. The truth is in there: Improving reasoning with layer-selective rank reduction PSharma JTAsh DMisra The Twelfth International Conference on Learning Representations, 2024b 29 18
342. Shazeer N. (2020). Glu variants improve transformer. ArXiv, pp. 16.
343. Shrikumar A., Greenside P. & Kundaje A. (2017). Learning important features through propagating activation differences.
344. Shrikumar A., Su J. & Kundaje A. (2018). Computationally efficient measures of internal neuron importance.
345. Siegel N. Y., Camburu O., Heess N. et al. (2024). The probabilities also matter: A more faithful metric for faithfulness of free-text explanations in large language models.
346. Simonyan K., Vedaldi A. & Zisserman A. (2014). Deep inside convolutional networks: Visualising image classification models and saliency maps.
347. Singh A. K., Moskovitz T., Hill F. et al. (2024). What needs to go right for an induction head? a mechanistic study of in-context learning circuits and their formation.
348. Singh C., Inala J. P., Galley M. et al. (2024). Rethinking interpretability in the era of large language models.
349. Singh S., Ravfogel S., Herzig J. et al. (2024). Mimic: Minimally modified counterfactuals in the representation space. Arxiv, pp. 15.
350. Sixt L., Granz M. & Landgraf T. (2020). When explanations lie: Why many modified BP attributions fail.
351. Smilkov D., Thorat N., Kim B. et al. (2017). Smoothgrad: removing noise by adding noise.
352. Smolensky P. (1986). Neural and conceptual interpretation of PDP models.
353. Stoehr N., Gordon M., Zhang C. et al. (2024). Localizing paragraph memorization in language models.
354. Stolfo A., Belinkov Y. & Sachan M. (2023). A mechanistic interpretation of arithmetic reasoning in language models using causal mediation analysis. DOI: 10.18653/v1/2023.emnlp-main.435
355. Stolfo A., Belinkov Y. & Sachan M. (2023). Understanding arithmetic reasoning in language models using causal mediation analysis. Arxiv, pp. 26.
356. Stolfo A., Wu B., Gurnee W. et al. (2024). Confidence regulation neurons in language models. ArXiv, pp. 24.
357. Suau X., Zappella L. & Apostoloff N. (2020). Finding experts in transformer models.
358. Suau X., Zappella L. & Apostoloff N. (2022). Self-conditioning pre-trained language models.
359. Sun M., Chen X., Kolter J. Z. et al. (2024). Massive activations in large language models.
360. Sundararajan M., Taly A. & Yan Q. (2017). Axiomatic attribution for deep networks.
361. Syed A., Rager C. & Conmy A. (2023). Attribution patching outperforms automated circuit discovery. Arxiv, pp. 12.
362. Takase S., Kiyono S., Kobayashi S. et al. (2023). B2T connection: Serving stability and performance in deep transformers. DOI: 10.18653/v1/2023.findings-acl.192
363. Tang T., Luo W., Huang H. et al. (2024). Language-specific neurons: The key to multilingual capabilities in large language models.
364. Tarzanagh D. A., Li Y., Thrampoulidis C. et al. (2024). Transformers as support vector machines.
365. GTeam MRiviere SPathak PGSessa CHardin SBhupatiraju LHussenot TMesnard BShahriari ARamé JFerret PLiu PTafti AFriesen MCasbon SRamos RKumar CLLan SJerome ATsitsulin NVieillard PStanczyk SGirgin NMomchev MHoffman SThakoor J.-BGrill BNeyshabur OBachem AWalton ASeveryn AParrish AAhmad AHutchison AAbdagic ACarl AShen ABrock ACoenen ALaforge APaterson BBastian BPiot BWu BRoyal CChen CKumar CPerry CWelty CAChoquette-Choo DSinopalnikov DWeinberger DVijaykumar DRogozińska DHerbison EBandy EWang ENoland EMoreira ESenter EEltyshev FVisin GRasskin GWei GCameron GMartins HHashemi HKlimczak-Plucińska HBatra HDhand INardini JMein JZhou JSvensson JStanway JChan JPZhou JCarrasqueira JIljazi JBecker JFernandez JVan Amersfoort JGordon JLipschultz JNewlan JJi KMohamed KBadola KBlack KMillican KMcdonell KNguyen KSodhia KGreene LLSjoesund LUsui LSifre LHeuermann LLago LMcnealus LBSoares LKilpatrick LDixon LMartins MReid MSingh MIverson MGörner MVelloso MWirth MDavidow MMiller MRahtz MWatson MRisdal MKazemi MMoynihan MZhang MKahng MPark MRahman MKhatwani NDao NBardoliwalla NDevanathan NDumai NChauhan OWahltinez PBotarda PBarnes PBarham PMichel PJin PGeorgiev PCulliton PKuppala RComanescu RMerhej RJana RARokni RAgarwal RMullins SSaadat SMCarthy SPerrin SM RArnold SKrause SDai SGarg SSheth SRonstrom SChan TJordan TYu TEccles THennigan TKocisky TDoshi VJain VYadav VMeshram VDharmadhikari WBarkley WWei WYe WHan WKwon XXu ZShen ZGong ZWei VCotruta PKirk ARao MGiang LPeran TWarkentin ECollins JBarral ZGhahramani RHadsell DSculley JBanks ADragan SPetrov OVinyals JDean DHassabis KKavukcuoglu CFarabet EBuchatskaya SBorgeaud NFiedel AJoulin KKenealy RDadashi AAndreev 17 Gemma 2: Improving open language models at a practical size. arXiv, 2024
366. Circuits updates -february 2024. update on dictionary learning improvements ATempleton TConerly JMarcus THenighan AGolubeva TBricken Transformer Circuits Thread, 2024a 57
367. ATempleton TConerly JMarcus JLindsey TBricken BChen APearce CCitro EAmeisen AJones HCunningham NLTurner CMcdougall MMacdiarmid CDFreeman TRSumers ERees JBatson AJermyn SCarter COlah THenighan Scaling monosemanticity: Extracting interpretable features from claude 3 sonnet. Transformer Circuits Thread, 2024b 25
368. Tenney I., Das D. & Pavlick E. (2019). BERT rediscovers the classical NLP pipeline. DOI: 10.18653/v1/P19-1452
369. Tenney I., Xia P., Chen B. et al. (2019). What do you learn from context? probing for sentence structure in contextualized word representations.
370. Tenney I., Wexler J., Bastings J. et al. (2020). The language interpretability tool: Extensible, interactive visualizations and analysis for NLP models. DOI: 10.18653/v1/2020.emnlp-demos.15
371. Tenney I., Mullins R., Du B. et al. (2024). Interactive prompt debugging with sequence salience. Arxiv, pp. 30.
372. Tian Y., Wang Y., Chen B. et al. (2023). Scan and snap: Understanding training dynamics and token composition in 1-layer transformer.
373. Tian Y., Wang Y., Zhang Z. et al. (2024). JoMA: Demystifying multilayer transformers via joint dynamics of MLP and attention.
374. Tibshirani R. (1996). Regression shrinkage and selection via the lasso. Journal of the Royal Statistical Society: Series B (Methodological), Vol. 58(1), pp. 16. DOI: 10.1111/j.2517-6161.1996.tb02080.x
375. Tigges C., Hollinsworth O. J., Geiger A. et al. (2023). Linear representations of sentiment in large language models. Arxiv, pp. 25.
376. Timkey W. & Van Schijndel M. (2021). All bark and no bite: Rogue dimensions in transformer language models obscure representational quality. DOI: 10.18653/v1/2021.emnlp-main.372
377. Todd E., Li M., Sharma A. S. et al. (2024). LLMs represent contextual tasks as compact function vectors.
378. Touvron H., Martin L., Stone K. et al. (2023). Llama 2: Open foundation and fine-tuned chat models. Arxiv.
379. Tufanov I., Hambardzumyan K., Ferrando J. et al. (2024). Lm transparency tool: Interactive tool for analyzing transformer language models. Arxiv, pp. 31.
380. Turner A. M., Thiergart L., Udell D. et al. (2023). Activation addition: Steering language models without optimization.
381. Turpin M., Michael J., Perez E. et al. (2023). Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting.
382. AVariengien Some common confusion about induction heads. Less Wrong, 2023 21
383. Variengien A. & Winsor E. (2023). Look before you leap: A universal emergent decomposition of retrieval tasks in language models.
384. Varma V., Shah R., Kenton Z. et al. (2023). Explaining grokking through circuit efficiency.
385. Varshney N., Yao W., Zhang H. et al. (2023). A stitch in time saves nine: Detecting and mitigating hallucinations of llms by validating low-confidence generation.
386. Vasconcelos H., Jörke M., Grunde-Mclaughlin M. et al. (2023). Explanations can reduce overreliance on ai systems during decision-making. Proc. ACM Hum.-Comput. Interact, Vol. 7(1), pp. 32. DOI: 10.1145/3579605
387. Vaswani A., Shazeer N., Parmar N. et al. (2017). Attention is all you need.
388. Veit A., Wilber M. & Belongie S. (2016). Residual networks behave like ensembles of relatively shallow networks.
389. Vig J. (2019). A multiscale visualization of attention in the transformer model. DOI: 10.18653/v1/P19-3007
390. Vig J. & Belinkov Y. (2019). Analyzing the structure of attention in a transformer language model. DOI: 10.18653/v1/W19-4808
391. Vig J., Gehrmann S., Belinkov Y. et al. (2020). Investigating gender bias in language models using causal mediation analysis.
392. Voita E. & Titov I. (2020). Information-theoretic probing with minimum description length. DOI: 10.18653/v1/2020.emnlp-main.14
393. Voita E., Sennrich R. & Titov I. (2019). The bottom-up evolution of representations in the transformer: A study with machine translation and language modeling objectives. DOI: 10.18653/v1/D19-1448
394. Voita E., Talbot D., Moiseev F. et al. (2019). Analyzing multi-head self-attention: Specialized heads do the heavy lifting, the rest can be pruned. DOI: 10.18653/v1/P19-1580
395. Voita E., Sennrich R. & Titov I. (2021). Analyzing the source and target contributions to predictions in neural machine translation. DOI: 10.18653/v1/2021.acl-long.91
396. EVoita JFerrando CNalmpantis Neurons in large language models: Dead, n-gram, positional. arXiv, 2023 14 25
397. Von Oswald J., Niklasson E., Randazzo E. et al. (2023). Transformers learn in-context by gradient descent.
398. Interpretability in the wild: a circuit for indirect object identification in GPT-2 small KRWang AVariengien AConmy BShlegeris JSteinhardt The Eleventh International Conference on Learning Representations, 2023a 10, 11, 12, 20, 26, 27 9
399. Wang T., Anikina N., Feldhus J. et al. (2024). Llmcheckup: Conversational examination of large language models via interpretability tools.
400. Wang S., Zhu Y., Liu H. et al. (2023). Knowledge editing for large language models: A survey.
401. Wang X., Wen K., Zhang Z. et al. (2022). Finding skill neurons in pre-trained transformer-based language models. DOI: 10.18653/v1/2022.emnlp-main.765
402. Wei D., Nair R., Dhurandhar A. et al. (2022). On the safety of interpretable machine learning: A maximum deviation approach.
403. Weiss G., Goldberg Y. & Yahav E. (2021). Thinking like transformers.
404. Wen K., Li Y., Liu B. et al. (2023). Transformers are uninterpretable with myopic methods: a case study with bounded dyck grammars.
405. Wichers N., Denison C. & Beirami A. (2024). Gradient-based language model red teaming.
406. Wolf T., Debut L., Sanh V. et al. (2020). Transformers: State-of-the-art natural language processing. DOI: 10.18653/v1/2020.emnlp-demos.6
407. Wright B. & Sharkey L. (2024). Addressing feature suppression in saes.
408. Wu W., Wang Y., Xiao G. et al. (2024). Retrieval head mechanistically explains long-context factuality. Arxiv, pp. 29.
409. Causal proxy models for concept-based model explanations ZWu KD'oosterlinck AGeiger AZur CPotts Proceedings of the 40th International Conference on Machine Learning, ICML'23. JMLR.org, 2023a the 40th International Conference on Machine Learning, ICML'23. JMLR.org, 2023a 13
410. Wu A., Geiger T., Icard C. et al. (2023). Interpretability at scale: Identifying causal mechanisms in alpaca.
411. Wu A., Arora Z., Wang A. et al. (2024). Reft: Representation finetuning for language models.
412. Wu Z., Geiger A., Arora A. et al. (2024). pyvene: A library for understanding and improving pytorch models via interventions.
413. Wu A., Geiger J., Huang A. et al. (2024). A reply to makelov et al. (2023)'s "interpretability illusion" arguments.
414. Xiao G., Tian Y., Chen B. et al. (2023). Efficient streaming language models with attention sinks. Arxiv, pp. 22.
415. Xie S. M., Raghunathan A., Liang P. et al. (2022). An explanation of in-context learning as implicit bayesian inference.
416. Xiong R., Yang Y., He D. et al. (2020). On layer normalization in the transformer architecture.
417. Yang S., Huang S., Zou W. et al. (2023). Local interpretation of transformer based on linear decomposition. DOI: 10.18653/v1/2023.acl-long.572
418. Yao Y., Wang P., Tian B. et al. (2023). Editing large language models: Problems, methods, and opportunities. DOI: 10.18653/v1/2023.emnlp-main.632
419. Yin K. & Neubig G. (2022). Interpreting language models with contrastive explanations. DOI: 10.18653/v1/2022.emnlp-main.14
420. Yu J., Merullo E. & Pavlick (2023). Characterizing mechanisms for factual recall in language models. DOI: 10.18653/v1/2023.emnlp-main.615
421. White-box transformers via sparse rate reduction YYu SBuchanan DPai TChu ZWu STong BDHaeffele YMa Thirty-seventh Conference on Neural Information Processing Systems, 2023b 31
422. Yu Z. & Ananiadou S. (2024). Locating factual knowledge in large language models: Exploring the residual stream and analyzing subvalues in vocabulary space.
423. Yuksekgonul M., Chandrasekaran V., Jones E. et al. (2024). Attention satisfies: A constraint-satisfaction lens on factual errors of language models.
424. Zeiler M. D. & Fergus R. (2014). Visualizing and understanding convolutional networks.
425. Zhang B. & Sennrich R. (2019). Root mean square layer normalization.
426. Zhang F. & Nanda N. (2024). Towards best practices of activation patching in language models: Metrics and methods.
427. SZhang SRoller NGoyal MArtetxe MChen SChen CDewan MDiab XLi XVLin TMihaylov MOtt SShleifer KShuster DSimig PSKoura ASridhar TWang LZettlemoyer 2022 23 Opt: Open pre-trained transformer language models
428. Zhao Z. & Shan B. (2024). Reagent: A model-agnostic feature attribution method for generative language models.
429. Zheng C., Yin F., Zhou H. et al. (2024). On prompt-driven safeguarding for large language models. ArXiv, pp. 15.
430. Zhong Z., Liu Z., Tegmark M. et al. (2023). The clock and the pizza: Two stories in mechanistic explanation of neural networks.
431. Zhou B., Khosla A., Lapedriza A. et al. (2015). Object detectors emerge in deep scene cnns.
432. Zhou H., Bradley A., Littwin E. et al. (2024). What algorithms can transformers learn? a study in length generalization.
433. Zou A., Phan L., Chen S. et al. (2023). An alternative approach to resampling is ghost gradients (Jermyn & Templeton, 2024), which adds an auxiliary loss term that supplies a gradient signal to promote the reactivation of dead features. However, recent results have found this approach suboptimal. Arxiv, Vol. 15, pp. 14.
434. Setting the β 1 parameter of Adam to 0 has been found to reduce the number of "dead features in larger autoencoders (Templeton et al., 2024a; Rajamanoharan et al., 2024a
435. Conerly Yet 2024 rely on β 1 = 0.9
436. Conerly (2024). Although intially the norm of the decoder's rows 24 was recommended to be equal to one (Bricken et al., 2023), recent released SAEs also consider an unconstrained norm setting.
