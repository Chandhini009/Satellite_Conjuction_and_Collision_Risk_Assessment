#Connect 02_orbit_propogation.ipynb

from skyfield.api import load
from datetime import datetime, timezone
import pandas as pd

def propagate_satellite(satellite, hours=24):
    """
    Propagate a single satellite for the next 'hours' hours
    Returns DataFrame with Hour, Latitude, Longitude
    """
    ts = load.timescale()
    start = datetime.now(timezone.utc)
    positions = []
    for i in range(hours):
        t = ts.utc(start.year, start.month, start.day, start.hour + i)
        geocentric = satellite.at(t)
        subpoint = geocentric.subpoint()
        positions.append({
            "Hour": i,
            "Latitude": subpoint.latitude.degrees,
            "Longitude": subpoint.longitude.degrees
        })
    df_orbit = pd.DataFrame(positions)
    return df_orbit
