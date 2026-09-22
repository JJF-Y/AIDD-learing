import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import pandas as pd
from io import StringIO

url = 'https://huggingface.co/datasets/scikit-fingerprints/TDC_caco2_wang/resolve/main/tdc_caco2_wang.csv'
r = requests.get(url, timeout=60)
print(f'状态码: {r.status_code}')
print(f'文件大小: {len(r.content)} 字节')

if len(r.content) > 1000:
    df = pd.read_csv(StringIO(r.text))
    print(f'数据形状: {df.shape}')
    print(f'列名: {df.columns.tolist()}')
    print(df.head())
    print('\n标签统计:')
    if 'Y' in df.columns:
        print(df['Y'].describe())
    elif 'y' in df.columns:
        print(df['y'].describe())
    else:
        print(df.iloc[:, -1].describe())
    # 保存到本地
    with open('caco2_wang.csv', 'wb') as f:
        f.write(r.content)
    print('\n已保存到 caco2_wang.csv')
else:
    print('内容太小:')
    print(r.text[:300])