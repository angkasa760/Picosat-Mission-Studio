import numpy as np
import matplotlib.pyplot as plt

def analyze_doppler_shift():
    # --- Constants ---
    f_c = 437.2e6  # Hz (Carrier Frequency)
    v_c = 3e8      # m/s (Speed of Light)
    r_earth = 6371 # km
    h_orbit = 400  # km (Typical LEO)
    g = 6.67430e-20 * 5.972e24 # GM constant (km^3/s^2)
    
    # --- Orbital Velocity (m/s) ---
    v_s = np.sqrt(g / (r_earth + h_orbit)) * 1000 # m/s (Circular orbit)
    print(f"Orbital Velocity: {v_s:.2f} m/s (~{v_s/1000:.2f} km/s)")
    
    # --- Max Doppler Shift (Radial velocity max at horizon) ---
    delta_f_max = f_c * (v_s / v_c)
    print(f"Maximum Doppler Shift (at horizon): {delta_f_max/1000:.2f} kHz")
    
    # --- Doppler Profile Over Time ---
    # Simplified relative radial velocity during a 10-minute pass
    t = np.linspace(-300, 300, 600)  # -5 to +5 minutes from zenith
    d_theta_dt = v_s / (r_earth + h_orbit) # angular velocity
    
    theta = d_theta_dt * t
    # Approximate radial velocity relative to ground observer
    v_r = v_s * np.sin(theta) # This assumes GS is on the orbital plane (simplified)
    
    f_doppler = f_c * (1 - v_r / v_c)
    shift_khz = (f_doppler - f_c) / 1000

    plt.figure(figsize=(10, 6))
    plt.plot(t, shift_khz, 'r-', lw=2)
    plt.title(f'Doppler Shift Profile (UHF 437.2 MHz at {h_orbit}km Orbit)')
    plt.xlabel('Time from Zenith (seconds)')
    plt.ylabel('Doppler Shift (kHz)')
    plt.axhline(0, color='black', alpha=0.3)
    plt.axvline(0, color='black', alpha=0.3, linestyle='--')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Add Bandwidth markers (CST Report: 38 MHz bandwidth)
    # 38 MHz is huge compared to 10-20 kHz doppler shift!
    plt.annotate(f'Max Shift: ±{delta_f_max/1000:.2f} kHz', xy=(0, delta_f_max/1000), 
                 xytext=(50, delta_f_max/1000 + 1), arrowprops=dict(arrowstyle='->'))
    
    plt.savefig('doppler_analysis.png')
    print("Exported: doppler_analysis.png")

if __name__ == "__main__":
    analyze_doppler_shift()
