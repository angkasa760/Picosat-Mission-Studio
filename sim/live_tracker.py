import sys
import os
import time
import json
import requests
import math
import numpy as np
import pandas as pd
from skyfield.api import load, EarthSatellite, Topos
from datetime import datetime

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

from sim.picosat_config import TLE_URL, LIVE_COORDS_PATH, MISSION_DATA_PATH, F_HZ_NOM, G_TX_DBI_NOM, DE421_BSP_PATH, PASSES_CSV_PATH
from sim.physics_utils import calculate_fspl

KML_PATH = os.path.join(os.path.dirname(LIVE_COORDS_PATH), 'mission_path.kml')

def fetch_weather():
    try:
        r = requests.get("https://wttr.in/Jakarta?format=j1", timeout=5)
        w_data = r.json()
        curr = w_data['current_condition'][0]
        return {
            "temp": curr['temp_C'],
            "desc": curr['weatherDesc'][0]['value'],
            "precip": float(curr['precipMM']),
            "humidity": curr['humidity']
        }
    except:
        return {"temp": "28", "desc": "Clear", "precip": 0.0, "humidity": "75"}

def fetch_solar_flux():
    try:
        r = requests.get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json", timeout=5)
        s_data = r.json()
        return float(s_data[-1][1])
    except:
        return 2.0

def generate_kml(history):
    """Generate a KML file for Google Earth."""
    coords_str = "\n".join([f"{p[1]},{p[0]},{p[2]}" for p in history])
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>PIN-UHF Satellite Ground Track</name>
    <Style id="yellowLineGreenPoly">
      <LineStyle><color>7f00ffff</color><width>4</width></LineStyle>
      <PolyStyle><color>7f00ff00</color></PolyStyle>
    </Style>
    <Placemark>
      <name>Live Mission Path</name>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates>
{coords_str}
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
"""
    with open(KML_PATH, 'w') as f:
        f.write(kml_content)

def run_live_tracker():
    ts = load.timescale()
    planets = load(DE421_BSP_PATH)
    jakarta = Topos('6.2088 S', '106.8456 E')
    
    try:
        with open(MISSION_DATA_PATH, 'r') as f:
            m_data = json.load(f)
        g_tx, f_hz = m_data.get('gain_dbi', G_TX_DBI_NOM), m_data.get('frequency_target_mhz', F_HZ_NOM/1e6) * 1e6
    except:
        g_tx, f_hz = G_TX_DBI_NOM, F_HZ_NOM

    try:
        r = requests.get(TLE_URL, timeout=10)
        lines = r.text.strip().split('\n')
        sat_name, line1, line2 = lines[0].strip(), lines[1], lines[2]
    except:
        sat_name, line1, line2 = "FOSSASAT-2E24", "1 66780U 25276DV  26096.19295498  .00004250  00000+0  20973-3 0  9993", "2 66780  97.4207 170.8375 0005352  39.3720 320.7902 15.18421554 19489"

    satellite = EarthSatellite(line1, line2, sat_name, ts)
    battery_soc, path_history = 98.0, []
    
    weather, k_index, last_api_check = fetch_weather(), fetch_solar_flux(), time.time()

    print(f"Tracking {sat_name}... [ELITE + GOOGLE EARTH KML ACTIVE]")

    while True:
        try:
            now = time.time()
            if now - last_api_check > 300:
                weather, k_index, last_api_check = fetch_weather(), fetch_solar_flux(), now

            t = ts.now()
            geocentric = satellite.at(t)
            subpoint = geocentric.subpoint()
            
            # ADCS Tumbling
            spin_fading_db = 0.0
            tumbling_rate_rpm = 5.0 # Rotasi 5 RPM
            
            # Link Budget
            diff = (satellite - jakarta).at(t)
            dist_km, alt_deg = diff.distance().km, diff.altaz()[0].degrees
            
            margin = -99.9
            eps_load_w = 0.8 # Idle Load
            if alt_deg > 0:
                eps_load_w = 2.0 # Tx Load saat terlihat
                fspl = calculate_fspl(dist_km * 1000, f_hz)
                rain_loss = weather['precip'] * 0.5
                iono_loss = max(0, (k_index - 4) * 1.5) if k_index > 4 else 0.5
                
                # Efek Spin Fading (Polarization Loss) berdasar rotasi waktu nyata
                spin_phase = (now % 60.0) / 60.0 * 2 * math.pi * tumbling_rate_rpm
                spin_fading_db = -25.0 * (1.0 - abs(math.cos(spin_phase)))
                
                margin = (20.0 + g_tx - fspl + 12.0 - rain_loss - iono_loss + spin_fading_db) - (-137.0)
            
            # Power (EPS) System
            is_sunlit = geocentric.is_sunlit(planets)
            eps_gen_w = 1.5 if is_sunlit else 0.0
            eps_net_w = eps_gen_w - eps_load_w
            # Kapasitas baterai ~ 10 Wh. Perubahan Soc per 10 detik.
            battery_soc = max(0.0, min(100.0, battery_soc + (eps_net_w / 10.0 * 100.0 * (10.0/3600.0))))
            
            # History for KML
            path_history.append((subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.km))
            if len(path_history) > 500: path_history.pop(0)
            generate_kml(path_history)

            # Next Pass Detection
            next_pass = "N/A"
            try:
                pass_df = pd.read_csv(PASSES_CSV_PATH)
                now_dt = datetime.now()
                # Find first pass where Rise is in the future
                future_passes = pass_df[pd.to_datetime(pass_df['Rise']) > now_dt]
                if not future_passes.empty:
                    next_pass = future_passes.iloc[0]['Rise'].split(' ')[1][:5] + " UTC"
            except Exception as e:
                pass # Silently fail if schedule is missing

            # Export
            data = {
                "name": sat_name, "lat": round(subpoint.latitude.degrees, 4), "lon": round(subpoint.longitude.degrees, 4),
                "alt": round(subpoint.elevation.km, 2), "is_sunlit": bool(is_sunlit), "battery_soc": round(battery_soc, 2),
                "live_link_margin": round(margin, 2), "weather": weather, "k_index": k_index,
                "next_pass": next_pass, "alt_deg": round(alt_deg, 2),
                "eps_gen_w": eps_gen_w, "eps_load_w": eps_load_w,
                "spin_fading_db": round(spin_fading_db, 2), "tumbling_rate_rpm": tumbling_rate_rpm,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(LIVE_COORDS_PATH, 'w') as f: json.dump(data, f)
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}"); time.sleep(10)

if __name__ == "__main__":
    run_live_tracker()
