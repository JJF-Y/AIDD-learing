import os
import pandas as pd

DATA_URL = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv"
script_dir  = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir,'..','data','solubility_raw.csv')
log_path = os.path.join(script_dir,'..','data','01_summary.txt')

COL_SMILES = "smiles"
COL_TARGET = "measured log solubility in mols per litre"
COL_PRED = "ESOL predicted log solubility in mols per litre"

def load_raw(url):
    return pd.read_csv(url)

def select_columns(df):
    df = df[[COL_SMILES, COL_TARGET, COL_PRED]]
    df.columns = ["smiles", "y", "esol+pred"]
    return df

def main():
    df = load_raw(DATA_URL)
    print(f"原始形状:{df.shape}")
    df = select_columns(df)
    print(f"筛选后的形状：{df.shape}")
    print(f"{df['y'].describe()}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(log_path, 'w', encoding='utf_8') as f:
        f.write(f"shape: {df.shape}\n\n")
        f.write(df['y'].describe().to_string())
    print(f"日志已保存到：{log_path}")

if __name__ == "__main__":
    main()


