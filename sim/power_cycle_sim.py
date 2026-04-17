import numpy as np
import matplotlib.pyplot as plt

def analyze_power_cycle():
    # --- Satellite Parameters ---
    # FossaSat-1 based: ~1 Wh battery (3.7V, 300mAh)
    # Solar Panels: ~1W peak on 1 facet (50x50mm GaAs 30% eff)
    # Quiescent consumption: 50mW
    # Radio TX consumption: 500mW (during 10-min GS pass)
    
    battery_cap_wh = 1.11 # 300mAh * 3.7V
    soc_initial = 100 # %
    t_orbit = 90 # mins
    t_eclipse = 35 # mins (approx for 400km LEO)
    t_sunlight = t_orbit - t_eclipse
    
    # Simulation: 24 hours (1440 mins)
    dt = 1 # min
    time_mins = np.arange(0, 1440, dt)
    n_steps = len(time_mins)
    
    soc = np.zeros(n_steps)
    p_solar = np.zeros(n_steps)
    p_load = np.zeros(n_steps)
    
    curr_soc_wh = battery_cap_wh * (soc_initial / 100)
    
    # Simplified Ground Station Pass Windows (approx 4 passes per 24h)
    pass_times = [(120, 130), (520, 530), (920, 930), (1320, 1330)]
    
    for i in range(n_steps):
        t = time_mins[i]
        
        # 1. Solar Input (Sinusoidal in sunlight, 0 in eclipse)
        orbit_phase = (t % t_orbit)
        if orbit_phase < t_sunlight:
            # Solar power peaks when sun is normal to panel
            p_solar[i] = 1.2 * np.sin(np.pi * orbit_phase / t_sunlight)
        else:
            p_solar[i] = 0.0
            
        # 2. Load Consumption
        is_pass = any(start <= t <= end for start, end in pass_times)
        p_load[i] = 0.55 if is_pass else 0.08 # Watts (TX vs Standby)
        
        # 3. Energy Balance
        net_p = p_solar[i] - p_load[i]
        # Efficiency: 90% charge, 95% discharge
        if net_p > 0:
            curr_soc_wh += (net_p * 0.9) * (dt/60)
        else:
            curr_soc_wh += (net_p / 0.95) * (dt/60)
            
        # Clamp SoC
        curr_soc_wh = np.clip(curr_soc_wh, 0, battery_cap_wh)
        soc[i] = (curr_soc_wh / battery_cap_wh) * 100

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_mins / 60, soc, 'b-', lw=2, label='Battery SoC (%)')
    plt.axhline(60, color='red', linestyle='--', alpha=0.3, label='Safe Threshold')
    plt.title('24-Hour Orbital Power Cycle Analysis (SoC)')
    plt.ylabel('Charge (%)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.fill_between(time_mins / 60, p_solar, color='orange', alpha=0.3, label='Solar Production (W)')
    plt.plot(time_mins / 60, p_load, 'r-', lw=1, label='System Load (W)')
    plt.xlabel('Time (Hours)')
    plt.ylabel('Power (W)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('power_cycle_analysis.png')
    print("Exported: power_cycle_analysis.png")
    
    min_soc = np.min(soc)
    print(f"Minimum SoC: {min_soc:.2f}%")
    print(f"Energy Status: {'STABLE' if min_soc > 60 else 'CRITICAL'}")

if __name__ == "__main__":
    analyze_power_cycle()
