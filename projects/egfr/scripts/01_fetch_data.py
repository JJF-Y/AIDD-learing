"""
第1步：从 ChEMBL 数据库拉取 EGFR 的活性数据
用法：python 01_fetch_data.py
"""

import requests
import pandas as pd
import time
import os

# ChEMBL API 地址
BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

# 输出文件路径
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, '..', 'data', 'egfr_raw.csv')


def fetch_activities(target_chembl_id, max_records=5000):
    """拉取靶点的活性数据"""
    activities = []
    offset = 0
    limit = 1000  # 每次最多拉 1000 条
    
    while len(activities) < max_records:
        url = f"{BASE_URL}/activity.json"
        params = {
            'target_chembl_id': target_chembl_id,
            'limit': limit,
            'offset': offset,
        }
        
        print(f'正在拉取第 {offset+1}-{offset+limit} 条...')
        
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f'请求失败：{e}')
            break
        
        acts = data.get('activities', [])
        if not acts:
            print('没有更多数据了')
            break
        
        activities.extend(acts)
        offset += limit
        
        # 礼貌一点，别把人家服务器搞崩了
        time.sleep(0.5)
        
        if len(acts) < limit:
            break
    
    return activities[:max_records]


def parse_activities(activities):
    """把原始活性数据解析成表格"""
    rows = []
    for act in activities:
        row = {
            'molecule_chembl_id': act.get('molecule_chembl_id'),
            'smiles': act.get('canonical_smiles'),
            'standard_type': act.get('standard_type'),   # 活性类型（IC50, Ki, etc.）
            'standard_value': act.get('standard_value'), # 活性数值
            'standard_units': act.get('standard_units'),  # 单位（nM, uM, etc.）
            'standard_relation': act.get('standard_relation'),  # =, >, <
            'assay_chembl_id': act.get('assay_chembl_id'),
            'target_chembl_id': act.get('target_chembl_id'),
            'pchembl_value': act.get('pchembl_value'),   # pIC50 / pKi，换算好的对数
        }
        rows.append(row)
    
    return pd.DataFrame(rows)


def main():
    print('=' * 50)
    print('第1步：从 ChEMBL 拉取 EGFR 活性数据')
    print('=' * 50)
    
    # EGFR 靶点的 ChEMBL ID
    target_name = 'Epidermal growth factor receptor'
    target_chembl_id = 'CHEMBL203'
    print(f'使用靶点：{target_name} ({target_chembl_id})')
    
    # 拉取活性数据
    print(f'\n开始拉取活性数据...')
    activities = fetch_activities(target_chembl_id, max_records=5000)
    print(f'\n共拉取 {len(activities)} 条活性数据')
    
    if not activities:
        print('没拉到数据，退出')
        return
    
    # 解析成表格
    df = parse_activities(activities)
    print(f'\n数据形状：{df.shape}')
    print(f'\n活性类型分布：')
    print(df['standard_type'].value_counts().head(10))
    
    # 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f'\n原始数据已保存到：{output_path}')
    print(f'共 {len(df)} 条记录')


if __name__ == '__main__':
    main()
