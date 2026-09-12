#完整的一个，从数据加载到模型训练和评估，以及数据的可视化

#先简单捋一下思路，先获取药名，再根据药名获取药物的相关信息，然后进行数据清洗和预处理，最后进行模型训练和评估。同时尝试优化原有的思路

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)

from rdkit import Chem
from rdkit.Chem import Descriptors

import pubchempy as pcp

import time

import csv

import os

drug_names = [
    # 心血管-ACEI/ARB（18）
    'enalapril', 'lisinopril', 'perindopril', 'ramipril', 'quinapril',
    'benazepril', 'moexipril', 'trandolapril', 'captopril', 'fosinopril',
    'telmisartan', 'valsartan', 'irbesartan', 'losartan', 'olmesartan',
    'azilsartan', 'eprosartan', 'candesartan',
    # 心血管-CCB（12）
    'nifedipine', 'felodipine', 'nicardipine', 'nimodipine', 'amlodipine',
    'isradipine', 'lacidipine', 'lercanidipine', 'manidipine', 'cilnidipine',
    'verapamil', 'diltiazem',
    # 心血管-β受体阻滞剂（12）
    'bisoprolol', 'carvedilol', 'atenolol', 'nadolol', 'pindolol',
    'metoprolol', 'propranolol', 'acebutolol', 'esmolol', 'sotalol',
    'betaxolol', 'nebivolol',
    # 心血管-利尿剂（12）
    'hydrochlorothiazide', 'furosemide', 'spironolactone', 'eplerenone',
    'amiloride', 'triamterene', 'indapamide', 'chlorthalidone',
    'metolazone', 'acetazolamide', 'bumetanide', 'torsemide',
    # 心血管-α阻滞剂（6）
    'doxazosin', 'tamsulosin', 'terazosin', 'alfuzosin', 'silodosin',
    'prazosin',
    # 心血管-抗心律失常（8）
    'amiodarone', 'mexiletine', 'flecainide', 'propafenone', 'quinidine',
    'procainamide', 'disopyramide', 'dronedarone',
    # 心血管-抗凝抗血小板（10）
    'warfarin', 'dabigatran', 'rivaroxaban', 'apixaban', 'clopidogrel',
    'ticagrelor', 'prasugrel', 'ticlopidine', 'dipyridamole', 'cilostazol',
    # 心血管-降脂（12）
    'atorvastatin', 'rosuvastatin', 'simvastatin', 'pravastatin',
    'lovastatin', 'fluvastatin', 'gemfibrozil', 'fenofibrate',
    'bezafibrate', 'cholestyramine', 'ezetimibe', 'colesevelam',
    # 心血管-血管扩张（5）
    'hydralazine', 'minoxidil', 'sodium nitroprusside', 'isosorbide',
    'nitroglycerin',
    # 抗菌-青霉素类（10）
    'amoxicillin', 'ampicillin', 'cloxacillin', 'dicloxacillin',
    'flucloxacillin', 'piperacillin', 'ticarcillin', 'oxacillin',
    'nafcillin', 'carbenicillin',
    # 抗菌-头孢类（12）
    'cephalexin', 'cefaclor', 'cefixime', 'cefuroxime', 'cefotaxime',
    'ceftriaxone', 'cefepime', 'cefazolin', 'cefadroxil', 'cefpodoxime',
    'ceftazidime', 'cefdinir',
    # 抗菌-喹诺酮（8）
    'ciprofloxacin', 'norfloxacin', 'ofloxacin', 'moxifloxacin',
    'levofloxacin', 'gatifloxacin', 'sparfloxacin', 'lomefloxacin',
    # 抗菌-大环内酯（8）
    'azithromycin', 'clarithromycin', 'erythromycin', 'roxithromycin',
    'telithromycin', 'josamycin', 'spiramycin', 'midecamycin',
    # 抗菌-四环素（5）
    'tetracycline', 'doxycycline', 'minocycline', 'tigecycline',
    'oxytetracycline',
    # 抗菌-氨基糖苷（6）
    'gentamicin', 'tobramycin', 'kanamycin', 'amikacin', 'neomycin',
    'streptomycin',
    # 抗菌-其他（12）
    'clindamycin', 'metronidazole', 'tinidazole', 'nitrofurantoin',
    'chloramphenicol', 'linezolid', 'daptomycin', 'vancomycin',
    'teicoplanin', 'bacitracin', 'polymyxin', 'mupirocin',
    # 抗菌-碳青霉烯等（10）
    'ceftaroline', 'ceftobiprole', 'faropenem', 'ertapenem', 'meropenem',
    'imipenem', 'doripenem', 'aztreonam', 'quinupristin', 'dalfopristin',
    # 抗菌-新型（5）
    'tedizolid', 'oritavancin', 'dalbavancin', 'omadacycline',
    'plazomicin',
    # 抗真菌（15）
    'amphotericin', 'fluconazole', 'itraconazole', 'ketoconazole',
    'voriconazole', 'posaconazole', 'terbinafine', 'griseofulvin',
    'flucytosine', 'clotrimazole', 'isavuconazole', 'terconazole',
    'econazole', 'sertaconazole', 'naftifine',
    # 抗病毒（15）
    'acyclovir', 'valacyclovir', 'famciclovir', 'ganciclovir', 'ribavirin',
    'oseltamivir', 'zanamivir', 'sofosbuvir', 'entecavir', 'lamivudine',
    'zidovudine', 'abacavir', 'tenofovir', 'nevirapine', 'efavirenz',
    # 抗寄生虫（10）
    'mebendazole', 'albendazole', 'ivermectin', 'praziquantel',
    'chloroquine', 'hydroxychloroquine', 'quinine', 'pyrimethamine',
    'sulfadoxine', 'artemether',
    # 抗炎镇痛-NSAIDs（15）
    'aspirin', 'ibuprofen', 'diclofenac', 'naproxen', 'indomethacin',
    'sulindac', 'ketoprofen', 'flurbiprofen', 'piroxicam', 'meloxicam',
    'celecoxib', 'etodolac', 'nabumetone', 'ketorolac', 'mefenamic',
    # 镇痛-其他（5）
    'acetaminophen', 'nefopam', 'ziconotide', 'tapentadol',
    'dexketoprofen',
    # 镇痛-阿片（12）
    'morphine', 'codeine', 'tramadol', 'buprenorphine', 'methadone',
    'naloxone', 'naltrexone', 'fentanyl', 'oxycodone', 'hydromorphone',
    'meperidine', 'pentazocine',
    # 中枢-抗癫痫（15）
    'phenytoin', 'carbamazepine', 'valproate', 'lamotrigine',
    'gabapentin', 'pregabalin', 'topiramate', 'levetiracetam',
    'ethosuximide', 'primidone', 'oxcarbazepine', 'zonisamide',
    'vigabatrin', 'tiagabine', 'rufinamide',
    # 中枢-抗帕金森（8）
    'levodopa', 'carbidopa', 'amantadine', 'memantine', 'selegiline',
    'pramipexole', 'ropinirole', 'bromocriptine',
    # 中枢-痴呆（4）
    'donepezil', 'rivastigmine', 'galantamine', 'tacrine',
    # 中枢-抗抑郁（15）
    'fluoxetine', 'sertraline', 'paroxetine', 'citalopram',
    'escitalopram', 'venlafaxine', 'duloxetine', 'mirtazapine',
    'bupropion', 'amitriptyline', 'imipramine', 'nortriptyline',
    'clomipramine', 'trazodone', 'phenelzine',
    # 中枢-抗精神病（12）
    'olanzapine', 'clozapine', 'risperidone', 'quetiapine',
    'aripiprazole', 'ziprasidone', 'haloperidol', 'chlorpromazine',
    'fluphenazine', 'thioridazine', 'perphenazine', 'loxapine',
    # 中枢-抗焦虑（8）
    'alprazolam', 'diazepam', 'lorazepam', 'midazolam', 'zolpidem',
    'zopiclone', 'buspirone', 'chlordiazepoxide',
    # 中枢-其他（10）
    'suvorexant', 'modafinil', 'armodafinil', 'methylphenidate',
    'stiripentol', 'perampanel', 'retigabine', 'cannabidiol',
    'cenobamate', 'brivaracetam',
    # 消化系统（15）
    'omeprazole', 'pantoprazole', 'lansoprazole', 'rabeprazole',
    'famotidine', 'ranitidine', 'cimetidine', 'nizatidine',
    'misoprostol', 'metoclopramide', 'ondansetron', 'loperamide',
    'dexlansoprazole', 'bisacodyl', 'lactulose',
    # 呼吸系统（16）
    'salbutamol', 'terbutaline', 'salmeterol', 'formoterol',
    'budesonide', 'beclomethasone', 'fluticasone', 'montelukast',
    'theophylline', 'cromolyn', 'ipratropium', 'tiotropium',
    'indacaterol', 'olodaterol', 'vilanterol', 'glycopyrronium',
    # 内分泌-降糖（12）
    'metformin', 'glipizide', 'glyburide', 'glimepiride',
    'pioglitazone', 'rosiglitazone', 'repaglinide', 'nateglinide',
    'acarbose', 'sitagliptin', 'vildagliptin', 'canagliflozin',
    # 内分泌-甲状腺（5）
    'levothyroxine', 'methimazole', 'propylthiouracil', 'carbimazole',
    'liothyronine',
    # 皮质激素（10）
    'prednisone', 'prednisolone', 'dexamethasone', 'hydrocortisone',
    'betamethasone', 'triamcinolone', 'methylprednisolone',
    'fludrocortisone', 'fluocinolone', 'clobetasol',
    # 骨/内分泌其他（10）
    'raloxifene', 'alendronate', 'risedronate', 'ibandronate',
    'zoledronate', 'mifepristone', 'danazol', 'methyltestosterone',
    'fluoxymesterone', 'oxandrolone',
    # 抗肿瘤（40）
    'doxorubicin', 'paclitaxel', 'docetaxel', 'cisplatin', 'carboplatin',
    'oxaliplatin', 'fluorouracil', 'capecitabine', 'gemcitabine',
    'cyclophosphamide', 'ifosfamide', 'etoposide', 'topotecan',
    'irinotecan', 'vincristine', 'vinblastine', 'vinorelbine',
    'imatinib', 'erlotinib', 'gefitinib', 'sunitinib', 'sorafenib',
    'dasatinib', 'tamoxifen', 'letrozole', 'anastrozole', 'exemestane',
    'bicalutamide', 'temozolomide', 'methotrexate', 'pemetrexed',
    'raltitrexed', 'dacarbazine', 'procarbazine', 'lomustine',
    'carmustine', 'busulfan', 'melphalan', 'chlorambucil',
    'fludarabine',
    # 免疫抑制（8）
    'cyclosporine', 'tacrolimus', 'sirolimus', 'mycophenolate',
    'azathioprine', 'leflunomide', 'everolimus', 'mizoribine',
    # 抗组胺（14）
    'loratadine', 'cetirizine', 'fexofenadine', 'diphenhydramine',
    'chlorpheniramine', 'promethazine', 'clemastine', 'cyproheptadine',
    'hydroxyzine', 'dimenhydrinate', 'rupatadine', 'bilastine',
    'ebastine', 'terfenadine',
    # 泌尿（10）
    'tadalafil', 'sildenafil', 'vardenafil', 'finasteride',
    'dutasteride', 'oxybutynin', 'tolterodine', 'solifenacin',
    'mirabegron', 'darifenacin',
    # 止吐（5）
    'granisetron', 'palonosetron', 'dolasetron', 'aprepitant',
    'prochlorperazine',
    # 眼科（5）
    'latanoprost', 'bimatoprost', 'travoprost', 'brimonidine',
    'dorzolamide',
    # 皮肤外用（5）
    'hydroquinone', 'tretinoin', 'isotretinoin', 'acitretin',
    'calcipotriol',
    # 麻醉（10）
    'propofol', 'ketamine', 'thiopental', 'sevoflurane', 'isoflurane',
    'halothane', 'bupivacaine', 'ropivacaine', 'mepivacaine',
    'prilocaine',
    # 维生素（10）
    'thiamine', 'riboflavin', 'niacin', 'pyridoxine', 'cobalamin',
    'folate', 'ascorbic acid', 'cholecalciferol', 'retinol',
    'tocopherol',
    # 其他（10）
    'colchicine', 'allopurinol', 'febuxostat', 'probenecid',
    'sulfinpyrazone', 'penicillamine', 'dimercaprol', 'deferoxamine',
    'pralidoxime', 'edetate',
]
#为了避免每次测试都要重新获取，所以第一次获取后保存到本地，之后直接读取本地文件即可
#那么可以先做关于药物SMILES的获取的函数封装，然后再将运行结果进行本地保存

def get_drug_smiles(name_list, filename='drug_smiles.csv'):
    
    drug_smiles = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                drug_smiles[row[0]] = row[1]
    
    todo = [name for name in name_list if name not in drug_smiles]

    if not todo:
        print('全部已查询，直接读取缓存')
        return drug_smiles 
    print(f'已有 {len(drug_smiles)} 个，还需查询 {len(todo)} 个')

    for name in todo:
        for attempt in range(3):
            try:
                c = pcp.get_compounds(name, 'name')
                if c:
                    drug_smiles[name] = c[0].connectivity_smiles
                break
            except Exception:
                time.sleep(1)
                continue
        else:
            print(f'{name} 查询失败，跳过')
        time.sleep(0.3)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'SMILES'])
        for name, smiles in drug_smiles.items():
            writer.writerow([name, smiles])
    
    return drug_smiles

def calc_descriptors(drug_smiles):
    features = []
    labels = []
    for name,smiles in drug_smiles.items():
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f'{name} 解析失败')
            continue

        mw= Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hba  = Descriptors.NumHAcceptors(mol)
        hbd  = Descriptors.NumHDonors(mol)
        tpsa = Descriptors.TPSA(mol)
        rotatable = Descriptors.NumRotatableBonds(mol)
        fsp3 = Descriptors.FractionCSP3(mol)
        features.append([mw, logp, hba, hbd, tpsa, rotatable, fsp3])

        violations = 0
        if mw > 500:
            violations += 1
        if logp > 5:
            violations += 1
        if hba > 10:
            violations += 1
        if hbd > 5:
            violations += 1
        if tpsa > 140:
            violations += 1
        if rotatable > 10:
            violations += 1
        if fsp3 < 0.47:
            violations += 1
        labels.append(1 if violations <= 1 else 0)

    X = np.array(features)
    y = np.array(labels)
    return X,y

drug_smiles = get_drug_smiles(drug_names)

X,y = calc_descriptors(drug_smiles)
print(X.shape)
print(y.shape)

feature_names = ['MW', 'LogP', 'HBA', 'HBD', 'TPSA', 'RotatableBonds', 'Fsp3']

def model_fit(X,y,feature_names):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)

    scores = cross_val_score(model, X_train, y_train, cv=10)
    print(f'交叉验证准确率: {scores.mean():.2f} ± {scores.std():.2f}')

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f'准确率: {accuracy_score(y_test, y_pred):.2f}')

    importances = model.feature_importances_
    print("特征重要性:")
    for i, importance1 in enumerate(importances):
        print(f"  {feature_names[i]}: {importance1:.3f}")
    return model,X_test,y_test,y_pred

model,X_text,y_text,y_pred = model_fit(X, y, feature_names)

def evaluate_model(model, X_test, y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    print('混淆矩阵:')
    print(cm)
    print(classification_report(y_test, y_pred, target_names=['不合格', '合格']))
    return cm
CM = evaluate_model(model,X_text,y_text,y_pred)