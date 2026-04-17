import numpy as np
import matplotlib.pyplot as plt
import logging
from typing import Dict, Any

# Configure Professional Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_miles_rms(psd_g2_hz: float, fn_hz: float, q_factor: float) -> float:
    """
    Calculates the 1-DOF RMS response using Miles' Equation.
    
    Args:
        psd_g2_hz: Input Power Spectral Density (G^2/Hz) at natural frequency.
        fn_hz: Natural frequency of the component.
        q_factor: Transmissibility (Q) at resonance.
        
    Returns:
        G_rms response.
    """
    # Miles' Equation: Grms = sqrt(pi/2 * PSD * f * Q)
    g_rms = np.sqrt((np.pi / 2.0) * psd_g2_hz * fn_hz * q_factor)
    return g_rms

def analyze_vibration_survival() -> Dict[str, Any]:
    """
    Performs high-fidelity Structural Analysis using Miles' Equation for
    Random Vibration PSD and Static G-load superposition.
    """
    # --- Mechanical Parameters (Al 6061-T6) ---
    mat_yield_mpa = 276.0 # Yield Stress
    mat_density_kgm3 = 2700.0
    mass_kg = 0.25 # Total picosat mass
    wall_t_mm = 1.5
    side_len_mm = 50.0
    
    # --- Launch Profiles (GEVS Standard / SpaceX) ---
    # Random Vibration Profile: Input PSD level at first natural freq
    # Typical qualification levels: 14.1 Grms overall. 
    # Assume first fundamental mode at 500 Hz for CubeSats (conservative)
    fn_hz = 500.0
    psd_input = 0.1 # G^2/Hz (High level typical for picosats)
    q_factor = 10.0 # Standard Q for bolted aluminum structures
    
    static_g_load = 6.0 # Steady-state launch accel (axial)
    
    # 1. Random Vibration Response (Miles' Equation)
    g_rms_resp = calculate_miles_rms(psd_input, fn_hz, q_factor)
    
    # 2. Superposition of Loads (3-Sigma Peak)
    # Total Peak G = Static + 3 * Grms_Resp
    g_peak_total = static_g_load + (3.0 * g_rms_resp)
    f_peak_n = mass_kg * 9.81 * g_peak_total
    
    # 3. Stress Analysis (Plate Bending Approximation)
    # S_max = 0.5 * F / t^2 (Point center load assumption)
    stress_peak_mpa = 0.5 * f_peak_n / (wall_t_mm ** 2)
    
    # 4. Safety Factor & Margin
    factor_of_safety = mat_yield_mpa / stress_peak_mpa
    margin_of_safety = factor_of_safety - 1.0
    
    # Data Visual Rendering
    g_rms_range = np.linspace(1, 40, 100)
    stresses = 0.5 * (mass_kg * 9.81 * (static_g_load + 3 * g_rms_range)) / (wall_t_mm ** 2)
    
    plt.figure(figsize=(10, 6))
    plt.plot(g_rms_range, stresses, 'b-', lw=2, label='Peak Stress (3-Sigma)')
    plt.axhline(mat_yield_mpa, color='red', linestyle='--', label='Yield Strength (Al 6061-T6)')
    plt.axvline(g_rms_resp, color='green', linestyle=':', label='Calculated Response (Miles)')
    plt.fill_between(g_rms_range, 0, mat_yield_mpa, color='green', alpha=0.1, label='Elastic Region')
    
    plt.title('Advanced Random Vibration Survival (Miles Equation Analysis)')
    plt.xlabel('Response G_rms')
    plt.ylabel('Max Peak Stress (MPa)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.savefig('advanced_vibration_analysis.png')
    
    results = {
        "G_rms_Response": round(g_rms_resp, 2),
        "Total_Peak_G_3Sigma": round(g_peak_total, 2),
        "Max_Stress_MPa": round(stress_peak_mpa, 2),
        "MoS": round(margin_of_safety, 2),
        "Status": "STABLE" if margin_of_safety > 0 else "CRITICAL"
    }
    
    logger.info(f"Vibration Hardening Complete. MoS: {results['MoS']} (Status: {results['Status']})")
    return results

if __name__ == "__main__":
    res = analyze_vibration_survival()
    print(json.dumps(res, indent=4))
    
import json # Used for script runner print
