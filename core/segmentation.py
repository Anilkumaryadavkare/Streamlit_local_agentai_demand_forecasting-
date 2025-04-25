import pandas as pd
from sklearn.cluster import KMeans

def segment_demand(df: pd.DataFrame) -> dict:
    """
    Segment the demand data into clusters using KMeans.
    
    Args:
        df (pd.DataFrame): Input data with features for clustering.
    
    Returns:
        dict: A dictionary where keys are cluster IDs and values are data frames for each cluster.
    """
    print("[Step 2] Segmenting SKUs using KMeans...")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        print("[!] No numeric columns available for clustering.")
        df['cluster'] = 0
        return {0: df}

    n_clusters = min(4, len(df))  # Max 4 clusters or less based on rows
    if n_clusters < 1:
        raise ValueError("Insufficient data for segmentation.")

    try:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(df[numeric_cols])
        print(f"[✔] Segmentation complete: {n_clusters} clusters assigned.")
    except Exception as e:
        print(f"[✘] Clustering failed: {str(e)}")
        df['cluster'] = -1
        return {-1: df}

    # Split into dictionary of cluster dataframes
    segments = {cluster_id: group_df for cluster_id, group_df in df.groupby('cluster')}
    return segments
