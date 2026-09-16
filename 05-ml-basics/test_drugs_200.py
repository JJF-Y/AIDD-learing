# 外部验证集：200 个药名，与 drug_names_500 无重叠
# 类别：抗癌、抗病毒、抗真菌、免疫、靶向药等

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
    'alpelisib',           'piqray',             'olaparib',
    'rucaparib',           'niraparib',          'talazoparib',
    'talimogene',          'pembrolizumab',      'nivolumab',

    # 免疫检查点抑制剂（61-70）
    'atezolizumab',        'avelumab',           'durvalumab',
    'cemiplimab',          'ipilimumab',         'tremelimumab',
    'spartalizumab',       'dostarlimab',        'sintilimab',
    'tislelizumab',

    # 抗病毒（71-110）
    'abacavir',            'tenofovir',          'emtricitabine',
    'lamivudine',          'zidovudine',         'stavudine',
    'didanosine',          'zalcitabine',        'nevirapine',
    'efavirenz',           'etravirine',         'rilpivirine',
    'dolutegravir',        'raltegravir',        'elvitegravir',
    'maraviroc',           'enfuvirtide',        'boceprevir',
    'telaprevir',          'simeprevir',         'sofosbuvir',
    'ledipasvir',          'velpatasvir',        'voxilaprevir',
    'glecaprevir',         'pibrentasvir',       'dasabuvir',
    'ombitasvir',          'paritaprevir',       'ritonavir',

    # 更多抗病毒（111-130）
    'oseltamivir',         'zanamivir',          'peramivir',
    'baloxavir',           'remdesivir',         'molnupiravir',
    'nirmatrelvir',        'ritonavir',          'amantadine',
    'rimantadine',         'acyclovir',          'valacyclovir',
    'famciclovir',         'penciclovir',        'ganciclovir',
    'valganciclovir',      'cidofovir',          'foscarnet',
    'fomivirsen',          'palivizumab',

    # 抗真菌（131-160）
    'fluconazole',         'itraconazole',       'voriconazole',
    'posaconazole',        'isavuconazonium',    'ketoconazole',
    'miconazole',          'clotrimazole',       'econazole',
    'butoconazole',        'tioconazole',        'terconazole',
    'amphotericin',        'nystatin',           'caspofungin',
    'micafungin',          'anidulafungin',      'flucytosine',
    'terbinafine',         'griseofulvin',       'tolnaftate',
    'naftifine',           'butenafine',         'ciclopirox',
    'sertaconazole',       'oxiconazole',        'sulconazole',
    'econazole',           'luliconazole',       'efinaconazole',

    # 激素与内分泌（161-180）
    'tamoxifen',           'raloxifene',         'bazedoxifene',
    'ospemifene',          'anastrozole',        'letrozole',
    'exemestane',          'formestane',         'aminoglutethimide',
    'leuprolide',          'goserelin',          'triptorelin',
    'buserelin',           'nafarelin',          'histrelin',
    'degarelix',           'abarelix',           'flutamide',
    'bicalutamide',        'nilutamide',

    # 其他靶向/特殊（181-200）
    'thalidomide',         'lenalidomide',       'pomalidomide',
    'bortezomib',          'carfilzomib',        'ixazomib',
    'panobinostat',        'vorinostat',         'romidepsin',
    'belinostat',          'temsirolimus',       'tretinoin',
    'arsenic',             'hydroxyurea',        'procarbazine',
    'dacarbazine',         'temozolomide',       'lomustine',
    'carmustine',          'lomustine',
]
