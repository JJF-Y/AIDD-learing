"""
第1步：获取 ESOL 水溶性数据
用法：python 01_fetch_data.py
"""

import os
import pandas as pd

# ---------- 配置区：所有"外部信息"集中在这里 ----------
DATA_URL = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv"

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "..", "data", "solubility_raw.csv")
log_path = os.path.join(script_dir, "..", "data", "01_summary.txt")

COL_SMILES = "smiles"
COL_TARGET = "measured log solubility in mols per litre"
COL_PRED = "ESOL predicted log solubility in mols per litre"

def load_raw(url):
    """只管把表读进来，不筛选、不改名"""
    return pd.read_csv(url)

def select_columns(df):
    """只管选列和改名，不碰文件、不碰路径"""
    df = df[[COL_SMILES, COL_TARGET, COL_PRED]]
    df.columns = ["smiles", "y", "esol_pred"]
    return df

def main():
    print("=" * 50)
    print("第1步：拉取水溶性数据（ESOL / Delaney）")
    print("=" * 50)

    print(f"\n读取数据：{DATA_URL}")
    df = load_raw(DATA_URL)
    print(f"原始形状：{df.shape}")

    df = select_columns(df)
    print(f"筛选后形状：{df.shape}")

    print("\ny 的统计：")
    print(df["y"].describe())

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n已保存到：{output_path}")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"shape: {df.shape}\n\n")
        f.write(df["y"].describe().to_string())
    print(f"日志已保存到：{log_path}")

if __name__ == "__main__":
    main()