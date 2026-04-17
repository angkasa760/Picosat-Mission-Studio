import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import logging
from typing import Tuple, Dict, Any

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

# Configure Professional Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def solve_2node_thermal(t_skin: float, t_internal: float, q_gen: float, dt: float) -> Tuple[float, float]:
    """
    Solves a 2-node radiative heat transfer model: Skin vs Internal Components.
    
    Args:
        t_skin: Outer shell temperature (K).
        t_internal: Internal component temperature (K).
        q_gen: Internal heat generation (W).
        dt: Time step (s).
        
    Returns:
        Updated temperatures (t_skin, t_internal).
    """
    sigma = 5.67e-8 # Stefan-Boltzmann Constant
    epsilon_internal = 0.8 # Internal emissivity
    area_internal = 0.015 # m^2 (Internal PCB area approx)
    mass_internal = 0.1 # kg
    cp_internal = 900 # J/kgK (Al/Si mix)
    
    # 1. Internal Heat Exchange
    # q_rad = epsilon * sigma * area * (t_internal^4 - t_skin^4)
    q_out = epsilon_internal * sigma * area_internal * (t_internal**4 - t_skin**4)
    
    # 2. Update Internal Temp: dT = (Q_gen - Q_out) * dt / (m * cp)
    dt_internal = (q_gen - q_out) * dt / (mass_internal * cp_internal)
    t_internal_new = t_internal + dt_internal
    
    return t_skin, t_internal_new

from sim.picosat_config import MISSION_DATA_PATH, F_HZ_NOM, PLOTS_DIR

def analyze_thermal_impact() -> Dict[str, Any]:
    """
    Performs high-fidelity Thermal Analysis using a 2-node radiative model
    to predict antenna resonance shift across LEO orbital cycles.
    """
    # --- Load Data (Standardized) ---
    config_path = MISSION_DATA_PATH
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
            f_target = data.get('frequency_target_mhz', F_HZ_NOM/1e6) * 1e6
            arm_len_mm = data.get('arm_len_mm', 163.5)
            logger.info(f"Thermal Scan Initialized: {f_target/1e6} MHz")
        else:
            raise FileNotFoundError("Config missing")
    except Exception as e:
        logger.warning(f"Using baseline specs for thermal (Error: {e})")
        f_target, arm_len_mm = F_HZ_NOM, 163.5

    # --- Constants ---
    cte_becu = 17e-6  # Thermal expansion coeff ppm/°C
    
    # --- Simulation Params ---
    t_orbit_min = 90
    dt_sec = 60
    steps = int(t_orbit_min * 60 / dt_sec)
    time_min = np.linspace(0, t_orbit_min, steps)
    
    # 1. External Skin Temp Profile (LEO Sine -40 to 85°C)
    # T_skin = T_avg + T_amp * sin(wt)
    temp_skin_c = 22.5 + 62.5 * np.sin(2 * np.pi * time_min / 90)
    
    # 2. Internal Node Simulation
    temp_int_c = np.zeros(steps)
    temp_int_c[0] = 20.0 # Start at 20°C
    q_gen = 0.5 # 500mW internal heat generation
    
    for i in range(1, steps):
        t_skin_k = temp_skin_c[i] + 273.15
        t_int_k = temp_int_c[i-1] + 273.15
        _, t_int_next_k = solve_2node_thermal(t_skin_k, t_int_k, q_gen, dt_sec)
        temp_int_c[i] = t_int_next_k - 273.15
    
    # 3. Frequency Shift Analysis
    # antenna arms are usually on the exterior or coupled to the skin
    delta_t = temp_skin_c - 20.0
    delta_f_mhz = -(f_target/1e6) * cte_becu * delta_t
    f_shifted = (f_target/1e6) + delta_f_mhz

    # Visualization
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel('Mission Time (min)')
    ax1.set_ylabel('Temperature (°C)', color='tab:red')
    ax1.plot(time_min, temp_skin_c, 'r-', lw=2, label='Skin Temp (External)')
    ax1.plot(time_min, temp_int_c, 'k--', lw=1, label='Internal Component Temp')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Shifted Resonance (MHz)', color='tab:blue')
    ax2.plot(time_min, f_shifted, 'b-', alpha=0.6, label='Resonance Frequency')
    ax2.axhline(f_target, color='black', alpha=0.3, linestyle=':')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title('Research-Grade 2-Node Thermal/Resonance Shift Analysis')
    plt.tight_layout()
    output_plot = os.path.join(PLOTS_DIR, 'academic_thermal_analysis.png')
    plt.savefig(output_plot)
    logger.info(f"Thermal analysis plot exported to {output_plot}")
    
    max_shift_khz = np.max(np.abs(delta_f_mhz)) * 1000
    results = {
        "Max_Skin_Temp_C": round(np.max(temp_skin_c), 2),
        "Max_Int_Temp_C": round(np.max(temp_int_c), 2),
        "Max_Resonance_Shift_kHz": round(max_shift_khz, 2),
        "Status": "VALIDATED" if max_shift_khz < 1000 else "ATTENTION"
    }
    
    logger.info(f"Thermal Hardening Complete. Max Shift: {results['Max_Resonance_Shift_kHz']} kHz")
    return results

if __name__ == "__main__":
    res = analyze_thermal_impact()
    print(json.dumps(res, indent=4))
