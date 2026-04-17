import sys
import os
from skyfield.api import Topos, load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
import requests

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

from sim.picosat_config import PASSES_CSV_PATH, NORAD_ID, TLE_URL

def predict_passes():
    # --- Standardized Configuration ---
    tle_url = TLE_URL
    
    ts = load.timescale()
    try:
        print(f"Fetching Live TLE for Satellite {NORAD_ID}...")
        response = requests.get(tle_url, timeout=10)
        lines = response.text.strip().split('\n')
        if len(lines) < 3:
            raise ValueError("Invalid TLE response")
        
        name = lines[0].strip()
        line1 = lines[1].strip()
        line2 = lines[2].strip()
        print(f"Satellite Identified: {name}")
    except Exception as e:
        print(f"Update failed ({e}). Using offline baseline.")
        # ... fallback logic remains ...
        name = "FOSSASAT-2E24"
        line1 = "1 66780U 25276DV  26096.19295498  .00004250  00000+0  20973-3 0  9993"
        line2 = "2 66780  97.4207 170.8375 0005352  39.3720 320.7902 15.18421554 19489"

    satellite = EarthSatellite(line1, line2, name, ts)

    # Ground Station: Jakarta, Indonesia
    jakarta = Topos('6.2088 S', '106.8456 E')

    # Time range: Next 48 hours
    t0 = ts.now()
    t1 = ts.from_datetime(t0.utc_datetime() + timedelta(days=2))

    # Find passes
    t, events = satellite.find_events(jakarta, t0, t1, altitude_degrees=10.0)

    pass_data = []
    current_pass = {}
    
    for ti, event in zip(t, events):
        name = ('Rise', 'Culmination', 'Set')[event]
        time_str = ti.utc_strftime('%Y-%m-%d %H:%M:%S UTC')
        
        if event == 0: # Rise
            current_pass = {'Rise': time_str}
        elif event == 1: # Culmination
            current_pass['Culmination'] = time_str
            # Calculate max elevation
            difference = satellite - jakarta
            topocentric = difference.at(ti)
            alt, az, distance = topocentric.altaz()
            current_pass['Max Elevation'] = f"{alt.degrees:.1f}°"
        elif event == 2: # Set
            current_pass['Set'] = time_str
            pass_data.append(current_pass)

    df = pd.DataFrame(pass_data)
    print("--- Upcoming Passes over Jakarta (Next 48h) ---")
    print(df.to_string(index=False))
    df.to_csv(PASSES_CSV_PATH, index=False)

if __name__ == "__main__":
    predict_passes()
