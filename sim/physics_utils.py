import numpy as np
import math

def calculate_fspl(dist_m: float, f_hz: float) -> float:
    """
    Standard Free Space Path Loss (FSPL) Formula.
    FSPL = 20*log10(d) + 20*log10(f) + 20*log10(4*pi/c)
    """
    c = 299792458
    if dist_m <= 0: return 0.0
    return 20 * math.log10(dist_m) + 20 * math.log10(f_hz) + 20 * math.log10(4 * math.pi / c)

def calculate_itu_losses(f_hz: float, el_deg: float) -> float:
    """
    Atmospheric Gas and Rain Attenuation (ITU-R)
    """
    if el_deg <= 0: return 99.9 # Horizon/Blocked
    
    f_ghz = f_hz / 1e9
    el_rad = np.radians(el_deg)
    
    # Gas Loss
    eo, ew, h_eff = 0.007, 0.001, 8.0
    a_gas = (eo + ew) * h_eff / np.sin(el_rad)
    
    # Rain Loss (Tropical)
    r001, k, alpha = 50.0, 0.00004, 1.0
    gamma_r = k * (r001 ** alpha)
    l_eff = 5.0 / np.sin(el_rad)
    a_rain = gamma_r * l_eff
    
    return float(a_gas + a_rain)

def calculate_doppler_shift(rel_vel_ms: float, f_hz: float) -> float:
    """
    Classical Doppler Shift Formula.
    """
    c = 299792458
    return (rel_vel_ms / c) * f_hz
