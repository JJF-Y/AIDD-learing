"""
第1步：从 ChEMBL 数据库拉取 COX-2 的活性数据
用法：python 01_fetch_data.py
"""

import requests
import pandas as pd
import time
import os

BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, '..', 'data', 'cox2_raw.csv')

def fetch_activities(target_chembl_id, max_records=5000):
    activities = []     #存放拉取到的活性数据
    offset = 0  #当前从第几条开始拉（页码）
    limit = 1000    # 每次最多拉 1000 条
    
    while len(activities) < max_records:
        url = f"{BASE_URL}/activity.json"
        params = {      #请求参数
            'target_chembl_id': target_chembl_id,   #需要的靶点ID
            'limit': limit,     #每次拉取的记录数
            'offset': offset,   #偏移量，从第几条开始拉
        }
        
        print(f'正在拉取第 {offset+1}-{offset+limit} 条...')
        
        try:    #发送请求并处理响应
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status() #检查响应状态码
            data = resp.json()  #把返回的 JSON 字符串解析成 Python 的字典/列表
        except Exception as e:
            print(f'请求失败：{e}')
            break
        
        acts = data.get('activities', [])   #[]是默认值，如果没有activities字段就返回空列表
        if not acts:
            print('没有更多数据了')
            break   #终止循环
        
        activities.extend(acts)
        offset += limit #翻页，因为要循环，每次要从上一次循环的最后一条开始拉取

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
    print('第1步：从 ChEMBL 拉取 Cox-2 活性数据')
    print('=' * 50)
    
    # Cox-2 靶点的 ChEMBL ID
    target_name = 'Cyclooxygenase 2'
    target_chembl_id = 'CHEMBL230'
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
