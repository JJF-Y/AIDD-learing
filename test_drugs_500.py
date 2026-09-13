# 外部验证集：500 个药名，与 drug_names_500 无重叠
# 类别：靶向抗癌、免疫、抗病毒、抗真菌、抗寄生虫、眼科、皮肤科、血液、内分泌等

test_drugs = [
    # 靶向抗癌（1-30）
    'gefitinib',           'erlotinib',          'afatinib',
    'osimertinib',         'icotinib',           'dacomitinib',
    'crizotinib',          'ceritinib',          'alectinib',
    'brigatinib',          'lorlatinib',         'entrectinib',
    'vemurafenib',         'dabrafenib',         'trametinib',
    'cobimetinib',         'binimetinib',        'encorafenib',
    'palbociclib',         'ribociclib',         'abemaciclib',
    'everolimus',          'temsirolimus',       'ridaforolimus',
    'regorafenib',         'sorafenib',          'sunitinib',
    'pazopanib',           'axitinib',           'lenvatinib',

    # 更多抗癌（31-60）
    'cabozantinib',        'vandetanib',         'ponatinib',
    'nilotinib',           'dasatinib',          'bosutinib',
    'imatinib',            'ruxolitinib',        'fedratinib',
    'pacritinib',          'midostaurin',        'gilteritinib',
    'quizartinib',         'venetoclax',         'ibrutinib',
    'acalabrutinib',       'zanubrutinib',       'tirabrutinib',
    'idelalisib',          'duvelisib',          'copanlisib',
    'alpelisib',           'olaparib',           'rucaparib',
    'niraparib',           'talazoparib',        'pembrolizumab',
    'nivolumab',           'atezolizumab',       'avelumab',

    # 免疫检查点 & 免疫治疗（61-80）
    'durvalumab',          'cemiplimab',         'ipilimumab',
    'tremelimumab',        'dostarlimab',        'sintilimab',
    'tislelizumab',        'camrelizumab',       'toripalimab',
    'carilizumabin',       'blinatumomab',       'inotuzumab',
    'gemtuzumab',          'brentuximab',        'rituximab',
    'trastuzumab',         'pertuzumab',         'bevacizumab',
    'cetuximab',           'panitumumab',

    # 抗病毒（81-130）
    'abacavir',            'tenofovir',          'emtricitabine',
    'lamivudine',          'zidovudine',         'stavudine',
    'didanosine',          'zalcitabine',        'nevirapine',
    'efavirenz',           'etravirine',         'rilpivirine',
    'dolutegravir',        'raltegravir',        'elvitegravir',
    'maraviroc',           'enfuvirtide',        'boceprevir',
    'telaprevir',          'simeprevir',         'sofosbuvir',
    'ledipasvir',          'velpatasvir',        'voxilaprevir',
    'glecaprevir',         'pibrentasvir',       'dasabuvir',
    'ombitasvir',          'paritaprevir',       'elbasvir',
    'grazoprevir',         'beclabuvir',         'daclatasvir',
    'asunaprevir',         'faldaprevir',        'vaniprevir',
    'lopinavir',           'atazanavir',         'darunavir',
    'fosamprenavir',       'tipranavir',         'saquinavir',
    'indinavir',           'nelfinavir',         'amprenavir',

    # 抗流感/抗新冠/其他抗病毒（131-150）
    'oseltamivir',         'zanamivir',          'peramivir',
    'baloxavir',           'remdesivir',         'molnupiravir',
    'nirmatrelvir',        'amantadine',         'rimantadine',
    'acyclovir',           'valacyclovir',       'famciclovir',
    'penciclovir',         'ganciclovir',        'valganciclovir',
    'cidofovir',           'foscarnet',          'fomivirsen',
    'palivizumab',         'ribavirin',

    # 抗真菌（151-180）
    'fluconazole',         'itraconazole',       'voriconazole',
    'posaconazole',        'isavuconazonium',    'ketoconazole',
    'miconazole',          'clotrimazole',       'econazole',
    'butoconazole',        'tioconazole',        'terconazole',
    'amphotericin',        'nystatin',           'caspofungin',
    'micafungin',          'anidulafungin',      'flucytosine',
    'terbinafine',         'griseofulvin',       'tolnaftate',
    'naftifine',           'butenafine',         'ciclopirox',
    'sertaconazole',       'oxiconazole',        'sulconazole',
    'luliconazole',        'efinaconazole',      'tavaborole',

    # 抗寄生虫（181-200）
    'mebendazole',         'albendazole',        'thiabendazole',
    'ivermectin',          'permethrin',         'malathion',
    'lindane',             'praziquantel',       'niclosamide',
    'chloroquine',         'hydroxychloroquine', 'mefloquine',
    'primaquine',          'quinine',            'quinidine',
    'artemisinin',         'artesunate',         'artemether',
    'lumefantrine',        'pyrimethamine',

    # 激素与内分泌（201-240）
    'tamoxifen',           'raloxifene',         'bazedoxifene',
    'ospemifene',          'anastrozole',        'letrozole',
    'exemestane',          'formestane',         'aminoglutethimide',
    'leuprolide',          'goserelin',          'triptorelin',
    'buserelin',           'nafarelin',          'histrelin',
    'degarelix',           'abarelix',           'flutamide',
    'bicalutamide',        'nilutamide',         'enzalutamide',
    'apalutamide',         'darolutamide',       'abiraterone',
    'galeterone',          'fulvestrant',        'toremifene',
    'clomiphene',          'letrozole',          'anastrozole',

    # 糖尿病新药（241-260）
    'sitagliptin',         'saxagliptin',        'linagliptin',
    'alogliptin',          'vildagliptin',       'dutogliptin',
    'teneligliptin',       'gemigliptin',        'anagliptin',
    'empagliflozin',       'dapagliflozin',      'canagliflozin',
    'ertugliflozin',       'ipragliflozin',      'tofogliflozin',
    'exenatide',           'liraglutide',        'semaglutide',
    'dulaglutide',         'lixisenatide',

    # 血液系统（261-280）
    'warfarin',            'dabigatran',         'rivaroxaban',
    'apixaban',            'edoxaban',           'betrixaban',
    'clopidogrel',         'prasugrel',          'ticagrelor',
    'cilostazol',          'dipyridamole',       'eptifibatide',
    'tirofiban',           'abciximab',          'heparin',
    'enoxaparin',          'dalteparin',         'tinzaparin',
    'fondaparinux',        'desirudin',

    # 更多血液 & 贫血（281-300）
    'epoetin',             'darbepoetin',        'methoxy',
    'ropeginterferon',     'eltrombopag',        'romiplostim',
    'anagrelide',          'hydroxyurea',        'deferoxamine',
    'deferasirox',         'deferiprone',        'ferric',
    'iron',                'cyanocobalamin',     'folic',
    'pyridoxine',          'thiamine',           'niacin',
    'pantothenic',         'biotin',

    # 眼科用药（301-330）
    'timolol',             'betaxolol',          'levobunolol',
    'carteolol',           'metipranolol',       'latanoprost',
    'travoprost',          'bimatoprost',        'unoprostone',
    'tafluprost',          'brimonidine',        'apraclonidine',
    'dorzolamide',         'brinzolamide',       'acetazolamide',
    'methazolamide',       'pilocarpine',        'atropine',
    'cyclopentolate',      'tropicamide',        'homatropine',
    'phenylephrine',       'naphazoline',        'tetrahydrozoline',
    'oxymetazoline',       'lodoxamide',         'cromolyn',
    'ketotifen',           'olopatadine',        'azelastine',

    # 皮肤科（331-360）
    'tacrolimus',          'pimecrolimus',       'hydrocortisone',
    'triamcinolone',       'betamethasone',      'clobetasol',
    'mometasone',          'desonide',           'fluocinonide',
    'halobetasol',         'calcipotriene',      'tazarotene',
    'adapalene',           'tretinoin',          'isotretinoin',
    'benzoyl',            'clindamycin',        'erythromycin',
    'mupirocin',           'retapamulin',        'bacitracin',
    'neomycin',            'polymyxin',          'silver',
    'coal',                'salicylic',          'urea',
    'lactic',              'glycolic',           'azelaic',

    # 呼吸系统（361-380）
    'fluticasone',         'budesonide',         'beclomethasone',
    'mometasone',          'ciclesonide',        'albuterol',
    'salmeterol',          'formoterol',         'vilanterol',
    'indacaterol',         'olodaterol',         'tiotropium',
    'ipratropium',         'aclidinium',         'umeclidinium',
    'glycopyrronium',      'montelukast',        'zafirlukast',
    'zileuton',            'cromolyn',

    # 更多呼吸 & 抗过敏（381-400）
    'diphenhydramine',     'cetirizine',         'levocetirizine',
    'fexofenadine',        'loratadine',         'desloratadine',
    'chlorpheniramine',    'brompheniramine',    'hydroxyzine',
    'promethazine',        'cyproheptadine',     'astemizole',
    'terfenadine',         'azelastine',         'olopatadine',
    'bepotastine',         'rupatadine',         'bilastine',
    'meclizine',           'dimenhydrinate',

    # 胃肠道（401-425）
    'omeprazole',          'esomeprazole',       'lansoprazole',
    'dexlansoprazole',     'rabeprazole',        'pantoprazole',
    'cimetidine',          'ranitidine',         'famotidine',
    'nizatidine',          'sucralfate',         'misoprostol',
    'metoclopramide',      'ondansetron',        'granisetron',
    'dolasetron',          'palonosetron',       'alosetron',
    'loperamide',          'diphenoxylate',      'atropine',
    'lubiprostone',        'linaclotide',        'plecanatide',
    'mesalamine',          'budesonide',

    # 泌尿生殖（426-440）
    'oxybutynin',          'tolterodine',        'solifenacin',
    'darifenacin',         'trospium',           'fesoterodine',
    'mirabegron',          'sildenafil',         'tadalafil',
    'vardenafil',          'avanafil',           'alprostadil',
    'finasteride',         'dutasteride',        'tamsulosin',

    # 骨骼/钙调节（441-460）
    'alendronate',         'risedronate',        'ibandronate',
    'zoledronic',          'pamidronate',        'etidronate',
    'clodronate',          'tiludronate',        'calcitonin',
    'teriparatide',        'abaloparatide',      'romosozumab',
    'denosumab',           'raloxifene',         'bazedoxifene',
    'menotropins',         'follitropin',        'lutropin',
    'choriogonadotropin',  'cabergoline',

    # 中枢神经（461-480）
    'sumatriptan',         'rizatriptan',        'zolmitriptan',
    'naratriptan',         'almotriptan',        'eletriptan',
    'frovatriptan',        'galcanezumab',       'erenumab',
    'fremanezumab',        'galantamine',        'rivastigmine',
    'memantine',           'donepezil',          'tacrine',
    'selegiline',          'rasagiline',         'safinamide',
    'pramipexole',         'ropinirole',

    # 更多神经 & 精神（481-500）
    'aripiprazole',        'quetiapine',         'risperidone',
    'ziprasidone',         'paliperidone',       'asenapine',
    'iloperidone',         'lurasidone',         'brexpiprazole',
    'cariprazine',         'esketamine',         'lumateperone',
    'vortioxetine',        'levomilnacipran',    'desvenlafaxine',
    'duloxetine',          'venlafaxine',        'mirtazapine',
    'trazodone',           'bupropion',
]
