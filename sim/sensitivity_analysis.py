import numpy as np
import matplotlib.pyplot as plt

def analyze_fabrication_sensitivity():
    # --- Physical Data (From CST Report) ---
    f_target = 437.2  # MHz
    arm_len_nominal = 163.5  # mm
    sensitivity_rate = 0.9  # MHz per mm (from CST report observations)
    
    # --- Variation Range ---
    # Tolerances: ±5mm (worst case for manual cutting)
    delta_l = np.linspace(-5.0, 5.0, 100) # mm
    arm_lens = arm_len_nominal + delta_l
    
    # f_res(L) = f_target - sensitivity_rate * delta_l
    # Correcting: longer arm -> lower frequency.
    f_resonances = f_target - (sensitivity_rate * delta_l)
    
    # --- VSWR Estimation (Mock Model) ---
    # VSWR = 1 + alpha * (f_actual - f_target)^2
    # Based on CST report VSWR bandwidth ~45MHz for VSWR < 2.0
    bw_vswr_2 = 45 # MHz
    alpha = (2.0 - 1.2) / (bw_vswr_2/2)**2 # simplified parabolic mismatch
    vswr = 1.2 + alpha * (f_resonances - f_target)**2

    # Plotting
    plt.figure(figsize=(10, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(arm_lens, f_resonances, 'm-', lw=2)
    plt.axhline(y=f_target, color='r', linestyle='--', alpha=0.5, label='Target 437.2 MHz')
    plt.axvline(x=arm_len_nominal, color='k', alpha=0.3, label='Nominal 163.5 mm')
    plt.title('Fabrication Sensitivity: Frequency vs Arm Length')
    plt.ylabel('Resonance (MHz)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    plt.subplot(2, 1, 2)
    plt.plot(arm_lens, vswr, 'b-', lw=2)
    plt.axhline(y=2.0, color='r', linestyle='--', label='VSWR < 2.0 Limit')
    plt.fill_between(arm_lens, 1, 2, color='green', alpha=0.1, label='Safe Zone')
    plt.xlabel('Fabricated Arm Length (mm)')
    plt.ylabel('Estimated VSWR')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig('sensitivity_analysis.png')
    print(f"Exported: sensitivity_analysis.png")
    
    # Calculate Tolerance
    safe_delta = (bw_vswr_2 / 2) / sensitivity_rate
    print(f"Max fabrication error for VSWR < 2.0: ±{safe_delta:.2f} mm")

if __name__ == "__main__":
    analyze_fabrication_sensitivity()
