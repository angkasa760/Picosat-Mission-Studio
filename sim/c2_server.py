import sys, os, time, json, math, random, threading
import matplotlib
matplotlib.use('Agg') # Render off-screen
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from skyfield.api import load, Topos
from datetime import datetime

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

from sim.picosat_config import WEB_DIR, DATA_DIR, F_HZ_NOM, G_TX_DBI_NOM, DE421_BSP_PATH
from sim.physics_utils import calculate_fspl

app = Flask(__name__, static_folder=WEB_DIR)

app.config['WEB_DIR'] = WEB_DIR

# --- SYSTEM STATE ---
c2_state = {
    "cme_active": False,
    "cme_timer": 0,
    "evade_active": False,
    "evade_timer": 0
}

telemetry_data = {}

# --- SSTV GENERATOR THREAD ---
def generate_sstv():
    sstv_path = os.path.join(WEB_DIR, 'sstv_latest.jpg')
    while True:
        try:
            plt.figure(figsize=(4, 3), facecolor='black')
            noise = np.random.rand(100, 150)
            
            if c2_state["cme_active"]:
                noise = np.random.rand(100, 150) * 10
                cmap_choice = 'hot'
                status = "WARNING: SOLAR RADIATION"
            else:
                # Fake earth horizon
                for i in range(100):
                    for j in range(150):
                        if i > 70 + 5*math.sin(j/20):
                            noise[i,j] = noise[i,j]*0.2 + 0.3 # Earth
                cmap_choice = 'bone'
                status = "CAM NOMINAL"

            plt.imshow(noise, cmap=cmap_choice, vmin=0, vmax=1)
            plt.axis('off')
            plt.text(5, 10, f"PICOSAT SSTV | {status} | T:{int(time.time())}", color='lime' if not c2_state["cme_active"] else 'red', fontsize=8)
            plt.tight_layout(pad=0)
            plt.savefig(sstv_path, bbox_inches='tight', pad_inches=0)
            plt.close()
        except Exception as e:
            print("SSTV Error:", e)
        time.sleep(15)

# --- ENGINE THREAD ---
def physics_engine_loop():
    global telemetry_data
    ts = load.timescale()
    planets = load(DE421_BSP_PATH)
    jakarta = Topos('6.2088 S', '106.8456 E', elevation_m=10)
    
    print("Loading Constellation Data...")
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    satellites = load.tle_file(url)
    sats = [s for s in satellites if s.model.satnum in [25544, 48274, 43908]] # ISS and others for robust testing
    if len(sats) < 3: sats = satellites[:3]
    
    sat_names = ["CONSTELLATION-ALPHA", "CONSTELLATION-BETA", "CONSTELLATION-GAMMA"]
    battery_socs = [95.0, 80.0, 100.0]

    weather = {"desc": "Clear", "precip": 0.0}
    k_index = 2.0
    
    while True:
        now = time.time()
        
        # --- CME (Solar Flare) Logic ---
        if c2_state["cme_timer"] > 0:
            c2_state["cme_timer"] -= 10
            if c2_state["cme_timer"] <= 0: c2_state["cme_active"] = False
        else:
            if random.random() < 0.02: # 2% chance CME
                c2_state["cme_active"] = True
                c2_state["cme_timer"] = 120 # 2 minutes
                
        # --- Evasion Logic ---
        evade_offset_km = 0
        if c2_state["evade_active"]:
            evade_offset_km = 5.0 # Boost 5km
            c2_state["evade_timer"] -= 10
            if c2_state["evade_timer"] <= 0: c2_state["evade_active"] = False

        t = ts.now()
        out_data = {
            "constellation": [],
            "c2_status": "CRITICAL CME STORM" if c2_state["cme_active"] else "NOMINAL",
            "evasion_mode": c2_state["evade_active"],
            "weather": {"desc": "Clear", "precip": 0.0},
            "k_index": 2.0,
            "next_pass": "18:45 UTC"
        }

        for i, satellite in enumerate(sats[:3]):
            geocentric = satellite.at(t)
            subpoint = geocentric.subpoint()
            diff = (satellite - jakarta).at(t)
            dist_km, alt_deg = diff.distance().km, diff.altaz()[0].degrees
            
            # Physics Math
            is_sunlit = geocentric.is_sunlit(planets)
            tumbling_rate_rpm = 5.0 + (10.0 if c2_state["cme_active"] else 0.0) # Spin faster during CME
            
            spin_phase = (now % 60.0) / 60.0 * 2 * math.pi * tumbling_rate_rpm
            spin_fading_db = -25.0 * (1.0 - abs(math.cos(spin_phase)))
            
            margin = -99.9
            eps_load_w = 0.8
            if alt_deg > 0:
                eps_load_w = 2.0
                fspl = calculate_fspl(dist_km * 1000, F_HZ_NOM)
                margin = (20.0 + G_TX_DBI_NOM - fspl + 12.0 + spin_fading_db) - (-137.0)
            
            if c2_state["cme_active"]:
                margin = -99.9 # Complete blackout
                eps_load_w += 3.0 # Radiation damage load
                
            eps_gen_w = 1.5 if is_sunlit else 0.0
            eps_net_w = eps_gen_w - eps_load_w
            battery_socs[i] = max(0.0, min(100.0, battery_socs[i] + (eps_net_w / 10.0 * 100.0 * (10.0/3600.0))))

            debris_warning = False
            debris_dist = 0
            if random.random() < 0.03:
                debris_warning = True
                debris_dist = random.uniform(20.0, 5000.0)
                
            iot_payload = None
            if -11.0 <= subpoint.latitude.degrees <= 6.0 and 95.0 <= subpoint.longitude.degrees <= 141.0:
                if random.random() < 0.3:
                    iot_payload = f"[{sat_names[i]}-NODE] Temp {random.randint(20, 35)}C"

            out_data["constellation"].append({
                "id": i,
                "name": sat_names[i],
                "lat": round(subpoint.latitude.degrees, 4),
                "lon": round(subpoint.longitude.degrees, 4),
                "alt": round(subpoint.elevation.km + evade_offset_km, 2),
                "alt_deg": round(alt_deg, 2),
                "is_sunlit": bool(is_sunlit),
                "battery_soc": round(battery_socs[i], 2),
                "live_link_margin": round(margin, 2),
                "eps_gen_w": round(eps_gen_w, 2),
                "eps_load_w": round(eps_load_w, 2),
                "spin_fading_db": round(spin_fading_db, 2),
                "tumbling_rate_rpm": tumbling_rate_rpm,
                "debris_warning": debris_warning,
                "debris_dist": round(debris_dist, 1),
                "iot_payload": iot_payload
            })
            
        telemetry_data = out_data
        time.sleep(10)

# --- FLASK ROUTES ---
@app.route('/')
def root():
    return send_from_directory(app.config['WEB_DIR'], 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['WEB_DIR'], filename)

@app.route('/telemetry')
def get_telemetry():
    return jsonify(telemetry_data)

@app.route('/command/evade', methods=['POST'])
def command_evade():
    global c2_state
    c2_state["evade_active"] = True
    c2_state["evade_timer"] = 60 # 1 Min evasion
    return jsonify({"status": "EVASION SEQUENCE INITIATED", "offset": 5.0})

if __name__ == '__main__':
    print("STARTING GOD MODE C2 SERVER...")
    threading.Thread(target=generate_sstv, daemon=True).start()
    threading.Thread(target=physics_engine_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, threaded=True)
