# Connect 03_conjunction_analysis.ipynb

import numpy as np
import pandas as pd
from datetime import datetime, timezone
from skyfield.api import load

def distance_km(sat1, sat2, t):
    p1 = sat1.at(t).position.km
    p2 = sat2.at(t).position.km
    return np.linalg.norm(p1 - p2)

def detect_conjunctions(stations, hours=6, step_min=10, threshold=500, subset=5):
    """
    Detects close approaches among top 'subset' satellites
    Returns DataFrame with Time, Satellite1, Satellite2, Distance_km
    """
    ts = load.timescale()
    start = datetime.now(timezone.utc)
    time_range = [ts.utc(start.year, start.month, start.day, start.hour, m)
                  for m in range(0, hours*60, step_min)]
    
    satellites = stations[:subset]  # small subset for demo
    conjunctions = []
    
    for i in range(len(satellites)):
        for j in range(i+1, len(satellites)):
            sat1, sat2 = satellites[i], satellites[j]
            for t in time_range:
                d = distance_km(sat1, sat2, t)
                if d < threshold:
                    conjunctions.append({
                        "Time": t.utc_datetime(),
                        "Satellite1": sat1.name,
                        "Satellite2": sat2.name,
                        "Distance_km": round(d,2)
                    })
    df = pd.DataFrame(conjunctions)
    return df
