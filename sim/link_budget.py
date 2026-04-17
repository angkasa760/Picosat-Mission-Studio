import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import logging
from typing import Dict, Any

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

# Configure Professional Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from sim.picosat_config import MISSION_DATA_PATH, F_HZ_NOM, G_TX_DBI_NOM, PLOTS_DIR
from sim.physics_utils import calculate_fspl, calculate_itu_losses

def calculate_link_budget() -> Dict[str, Any]:
    """
    Performs a high-fidelity Link Budget Analysis using real CST simulation data
    and ITU-R standard atmospheric models.
    """
    # --- Load Satellite Parameters ---
    try:
        with open(MISSION_DATA_PATH, 'r') as f:
            data = json.load(f)
        f_hz = data.get('frequency_target_mhz', F_HZ_NOM/1e6) * 1e6
        g_tx_dbi = data.get('gain_dbi', G_TX_DBI_NOM)
        logger.info(f"Connected to Mission Config: {f_hz/1e6} MHz")
    except Exception as e:
        logger.warning(f"Using baseline specs (Config error: {e})")
        f_hz, g_tx_dbi = F_HZ_NOM, G_TX_DBI_NOM

    # --- Constants ---
    c = 299792458
    k_boltzmann_dbw = -228.6 # dBW/K/Hz
    
    # --- System Parameters ---
    p_tx_dbm = 20.0  # 100mW
    l_tx_db = 1.2    # Transmission line losses
    g_rx_dbi = 12.0  # Ground station Yagi antenna
    l_rx_db = 1.5    # Receiver losses
    bw_hz = 125e3    # LoRa BW
    t_sys_k = 290    # Standard noise temp
    d_km_min = 400.0 # Nadir distance
    d_km_max = 2000.0# Horizon distance
    el_ops = 30.0    # Typical operational elevation

    # --- Multi-Distance Calculation ---
    dist_range = np.linspace(d_km_min, d_km_max, 100)
    
    # 1. Transmitter EIRP
    eirp_dbw = (p_tx_dbm - 30) + g_tx_dbi - l_tx_db
    
    # 2. Path Losses (Dynamic Propagation)
    fspl_db = np.array([calculate_fspl(d * 1000, f_hz) for d in dist_range])
    
    # Dynamic Atmospheric Loss based on Elevation
    # el_eff: Approx elevation based on distance (400km nadir, 2000km horizon)
    el_angles = np.linspace(90, 10, 100) 
    l_atm_db = np.array([calculate_itu_losses(f_hz, el) for el in el_angles])
    
    l_pol_db = 3.0   # Circular-Linear mismatch
    l_point_db = 0.5 # Beam pointing error
    
    # 3. Receiver Power (Pr)
    p_rx_dbw = eirp_dbw - fspl_db - l_atm_db - l_pol_db - l_point_db + g_rx_dbi - l_rx_db
    
    # 4. Noise Floor
    n_floor_dbw = k_boltzmann_dbw + 10 * np.log10(t_sys_k) + 10 * np.log10(bw_hz)
    
    # 5. Link Performance
    snr_db = p_rx_dbw - n_floor_dbw
    req_snr_db = -15.0 # LoRa SF12 threshold
    link_margin_db = snr_db - req_snr_db

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(dist_range, link_margin_db, 'b-', lw=2, label='Link Margin (dB)')
    plt.axhline(0, color='red', linestyle='--', alpha=0.5, label='Threshold (SF12)')
    plt.fill_between(dist_range, 0, link_margin_db, where=(link_margin_db > 0), color='green', alpha=0.1)
    plt.title(f'Research-Grade Link Budget Analysis ({f_hz/1e6:.1f} MHz Mission)')
    plt.xlabel('Slant Range (km)')
    plt.ylabel('Margin (dB)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    output_plot = os.path.join(PLOTS_DIR, 'academic_link_budget.png')
    plt.savefig(output_plot)
    logger.info(f"Link budget plot exported to {output_plot}")
    
    results = {
        "EIRP_dBW": round(eirp_dbw, 2),
        "FSPL_Min_dB": round(fspl_db[0], 2),
        "ITU_Loss_Max_dB": round(np.max(l_atm_db), 4),
        "Min_Snr_dB": round(snr_db[-1], 2),
        "Max_Margin_dB": round(link_margin_db[0], 2)
    }
    
    logger.info(f"Link Hardening Complete. Max Margin: {results['Max_Margin_dB']} dB")
    return results

if __name__ == "__main__":
    res = calculate_link_budget()
    print(json.dumps(res, indent=4))
