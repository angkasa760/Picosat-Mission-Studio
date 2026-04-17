import numpy as np
import scipy.io.wavfile as wav

def generate_beacon_audio():
    sample_rate = 44100
    duration_sec = 10
    t = np.linspace(0, duration_sec, sample_rate * duration_sec)
    
    # 437.2 MHz is radio freq, but we'll simulate the "Audio Downconverted" beacon
    # Typical Morse/Beacon audio is 800Hz - 1200Hz
    f_audio = 1000 # 1 kHz beep
    
    # Simple Morse Code: "FOSSA" (F: ..-. O: --- S: ... S: ... A: .-)
    # Dot: 0.1s, Dash: 0.3s
    pattern = [
        0.1, 0.1, 0.3, 0.1, 0.4, # F
        0.3, 0.3, 0.3, 0.4,      # O
        0.1, 0.1, 0.1, 0.4,      # S
        0.1, 0.1, 0.1, 0.4,      # S
        0.1, 0.3                 # A
    ]
    
    morse_mask = np.zeros_like(t)
    curr_t = 0.5 # start at 0.5s
    for duration in pattern:
        start_idx = int(curr_t * sample_rate)
        end_idx = int((curr_t + duration) * sample_rate)
        if end_idx < len(morse_mask):
            morse_mask[start_idx:end_idx] = 1.0
        curr_t += duration + 0.1 # pause between elements
        
    audio = 0.5 * morse_mask * np.sin(2 * np.pi * f_audio * t)
    
    # Add noise for "Realistic Space" feel
    noise = 0.05 * np.random.normal(0, 1, len(t))
    audio += noise
    
    # Normalize to 16-bit
    audio_int = (audio * 32767).astype(np.int16)
    wav.write('picosat_beacon.wav', sample_rate, audio_int)
    print("Exported: picosat_beacon.wav (Simulated UHF Beacon)")

if __name__ == "__main__":
    generate_beacon_audio()
