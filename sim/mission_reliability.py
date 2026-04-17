import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import json
import logging
import random
from typing import Dict, Any

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

# Configure Professional Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from sim.picosat_config import MISSION_DATA_PATH, F_HZ_NOM, S11_NOM, PLOTS_DIR

def run_monte_carlo(iterations: int = 10000) -> Dict[str, Any]:
    """
    Performs a Monte Carlo simulation of Mission Success Probability.
    Models RF, Thermal, and Deployment failure modes.
    """
    logger.info(f"Starting Mission Reliability Simulation ({iterations} cycles)...")
    
    # 1. Load Baseline Specs (Standardized)
    config_path = MISSION_DATA_PATH
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
            f_target = data.get('frequency_target_mhz', F_HZ_NOM/1e6)
            s11_nom = data.get('s11_simulated_db', S11_NOM)
        else:
            raise FileNotFoundError("Config missing")
    except Exception as e:
        logger.warning(f"Using baseline specs for reliability (Error: {e})")
        f_target, s11_nom = F_HZ_NOM/1e6, S11_NOM

    # 2. Failure Mode Probability Definitions
    p_deployment_arm = 0.98  # Prob of one arm deploying perfectly
    total_arms = 4
    
    # 3. Monte Carlo Loops
    success_count = 0
    margins = []
    
    for _ in range(iterations):
        # A. Deployment Reliability (Bernoulli trials for 4 arms)
        arms_deployed = np.random.binomial(n=1, p=p_deployment_arm, size=total_arms).sum()
        deployment_loss_db = (4 - arms_deployed) * 6.0 # 6dB loss per stuck arm
        
        # B. Thermal Resonance Shift (Normal distribution)
        # Shift can be +/- 250 kHz due to extreme LEO transients
        t_shift_mhz = np.random.normal(0, 0.45) 
        s11_penalty_db = 0
        if abs(t_shift_mhz) > 0.5: # 500kHz threshold
            s11_penalty_db = 5.0 # Mismatch loss
            
        # C. RF Fading / Ionospheric Scintillation (Log-normal)
        rf_fading_db = np.random.lognormal(mean=0, sigma=0.5) # ~1.5dB variance
        
        # D. Link Margin Calculation (Simplified)
        # Nominal margin 30.76 dB 
        current_margin_db = 30.76 - (deployment_loss_db + s11_penalty_db + rf_fading_db)
        
        # SUCCESS CRITERIA: Margin > 0 dB
        if current_margin_db > 0:
            success_count += 1
            
        margins.append(current_margin_db)

    # 4. Success Probability (PoMS)
    poms = (success_count / iterations) * 100
    
    # Visualization: Margin Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(margins, bins=50, color='royalblue', alpha=0.7, edgecolor='black')
    plt.axvline(0, color='red', linestyle='--', label='Fail/Pass Threshold')
    plt.title(f'Mission Link Margin Distribution (MC n={iterations})')
    plt.xlabel('Simulated Link Margin (dB)')
    plt.ylabel('Frequency (Mission Cycles)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    output_plot = os.path.join(PLOTS_DIR, 'mission_reliability_plot.png')
    plt.savefig(output_plot)
    logger.info(f"Reliability plot exported to {output_plot}")
    
    results = {
        "iterations": iterations,
        "poms_percent": round(poms, 2),
        "mean_margin_db": round(np.mean(margins), 2),
        "worst_case_margin_db": round(np.min(margins), 2),
        "p_deployment_success": round(p_deployment_arm**total_arms * 100, 2)
    }
    
    logger.info(f"Relability Simulation Complete. Probability of Mission Success: {poms:.2f}%")
    return results

if __name__ == "__main__":
    res = run_monte_carlo()
    print(json.dumps(res, indent=4))
