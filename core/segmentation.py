import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

def segment_demand(df: pd.DataFrame) -> dict:
    """
    Segment the demand data into clusters using KMeans.
    """
    print("[Step 2] Segmenting SKUs using KMeans...")

    # Handle missing values
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        print("[!] No numeric columns available for clustering.")
        df['cluster'] = 0
        return {0: df}

    # Impute missing values
    imputer = SimpleImputer(strategy='median')
    df_imputed = pd.DataFrame(
        imputer.fit_transform(df[numeric_cols]),  # ✅ Now uses the input `df`
        columns=numeric_cols
    )

    n_clusters = min(4, len(df_imputed))
    if n_clusters < 1:
        raise ValueError("Insufficient data for segmentation.")

    try:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(df_imputed)
        print(f"[✔] Segmentation complete: {n_clusters} clusters assigned.")
    except Exception as e:
        print(f"[✘] Clustering failed: {str(e)}")
        df['cluster'] = -1
        return {-1: df}
    # After clustering:
    segments = {cid: group for cid, group in df.groupby('cluster')}
    return {k: v for k, v in segments.items() if not v.empty}
    return segments