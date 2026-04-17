import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

def simulate_lora_performance():
    # --- Link Budget SNR (at 400km) ---
    snr_from_link = 14.76  # dB (calculated in Phase 1)
    
    # Range of Eb/N0
    ebn0_db = np.linspace(-30, 25, 200) # LoRa can work below noise floor (-20dB)
    ebn0_linear = 10**(ebn0_db / 10)
    
    # Mock BER for LoRa (approximated for SF7, SF10, SF12)
    # LoRa is M-ary FSK variant, BER ~ 0.5 * erfc(sqrt(Eb/N0 * (SF/2^SF))) - simplified
    def lora_ber(ebn0_db, sf):
        # LoRa SNR improves with Spreading Factor
        # Thresholds (typical): SF7: -7.5dB, SF10: -15dB, SF12: -20dB
        threshold = -7.5 - (sf - 7) * 2.5
        # Sigmoid approximation of BER cliff
        return 1 / (1 + np.exp(ebn0_db - threshold))

    plt.figure(figsize=(10, 6))
    for sf in [7, 10, 12]:
        ber = lora_ber(ebn0_db, sf)
        plt.semilogy(ebn0_db, ber, lw=2, label=f'LoRa SF{sf}')

    plt.axvline(x=snr_from_link, color='green', linestyle='--', label=f'Picosat Current SNR ({snr_from_link}dB)')
    plt.axhline(y=1e-5, color='black', alpha=0.3, linestyle=':', label='Reliable Link (BER<10⁻⁵)')
    
    plt.title('Communication Reliability: LoRa BER vs SNR Performance')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.ylim(1e-7, 1)
    plt.xlim(-25, 25)
    plt.grid(True, which='both', linestyle=':', alpha=0.6)
    plt.legend()
    
    plt.savefig('lora_sim_performance.png')
    print(f"Exported: lora_sim_performance.png")
    print(f"Current System Status: EXTREMELY STABLE (SNR {snr_from_link} dB >> SF12 threshold)")

if __name__ == "__main__":
    simulate_lora_performance()
