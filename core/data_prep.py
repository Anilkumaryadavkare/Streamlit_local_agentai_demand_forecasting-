import pandas as pd

def prepare_data(filepath):
    if isinstance(filepath, str):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_csv(filepath)

    df = df.drop_duplicates()

    for col in df.columns:
        if df[col].dtype == 'object':
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
        else:
            mean_val = df[col].mean()
            df[col] = df[col].fillna(mean_val)

    print(f"[✔] Cleaned {filepath}: {len(df)} rows, {len(df.columns)} columns.")
    return df
