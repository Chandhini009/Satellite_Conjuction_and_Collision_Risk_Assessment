# Connect 04_collision_summary.ipynb

import pandas as pd
import random

def compute_risk(df, threshold=500):
    """
    Input: df - DataFrame from conjunction analysis
    Output: df with additional 'Risk' column (0-1)
    """
    if df.empty:
        # Demo random risk if no real close approaches
        df = pd.DataFrame({
            "Time": pd.date_range(start=pd.Timestamp.now(), periods=10, freq='H'),
            "Satellite1": [f"Sat{i}" for i in range(1,11)],
            "Satellite2": [f"Sat{i+1}" for i in range(1,11)],
            "Distance_km": [random.randint(50, threshold) for _ in range(10)]
        })
    
    df['Risk'] = df['Distance_km'].apply(lambda x: max(0,(threshold-x)/threshold))
    return df
