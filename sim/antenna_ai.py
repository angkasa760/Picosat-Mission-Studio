import sys
import os
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib
import json

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

from sim.picosat_config import MISSION_DATA_PATH, F_HZ_NOM, S11_NOM, MODELS_DIR, PLOTS_DIR

def generate_synthetic_data():
    # --- Load Satellite Parameters (Standardized) ---
    config_path = MISSION_DATA_PATH
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            arm_len_nom = data.get('arm_len_mm', 163.5)
            f_nom = data.get('frequency_target_mhz', F_HZ_NOM/1e6)
            s11_nom = data.get('s11_simulated_db', S11_NOM)
        except Exception as e:
            print(f"Warning: Mission config corrupt ({e}). Using baselines.")
            arm_len_nom, f_nom, s11_nom = 163.5, F_HZ_NOM/1e6, S11_NOM
    else:
        arm_len_nom, f_nom, s11_nom = 163.5, F_HZ_NOM/1e6, S11_NOM

    sensitivity = 0.9 # MHz / mm
    
    # Generate 500 samples of arm_len variations
    arm_lens = np.linspace(150, 180, 500).reshape(-1, 1)
    
    # Model freq shift: shorter arm -> higher freq
    freqs = f_nom - sensitivity * (arm_lens - arm_len_nom)
    
    # Model S11: Perfect resonance at target f_nom
    delta_f = freqs - f_nom
    bw_mhz = 20 # 10dB bandwidth approx
    s11_vals = s11_nom + 30 * np.log10(1 + (np.abs(delta_f) / (bw_mhz/2))**2)
    s11_vals = np.clip(s11_vals, -25, -2) # realistic caps
    
    return arm_lens, s11_vals

def train_antenna_ai():
    X, y = generate_synthetic_data()
    
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)
    
    # MLP Regressor: 3 hidden layers for non-linear resonance curve
    model = MLPRegressor(hidden_layer_sizes=(64, 32, 16), max_iter=2000, random_state=42)
    model.fit(X_scaled, y_scaled.ravel())
    
    # Save models to dedicated folder
    joblib.dump(model, os.path.join(MODELS_DIR, 'antenna_model.pkl'))
    joblib.dump(scaler_X, os.path.join(MODELS_DIR, 'scaler_x.pkl'))
    joblib.dump(scaler_y, os.path.join(MODELS_DIR, 'scaler_y.pkl'))
    
    print(f"AI Model Trained Successfully. Models saved in: {MODELS_DIR}")
    
    # Verification Plot
    test_lens = np.linspace(155, 175, 50).reshape(-1, 1)
    test_scaled = scaler_X.transform(test_lens)
    preds_scaled = model.predict(test_scaled)
    preds = scaler_y.inverse_transform(preds_scaled.reshape(-1, 1))
    
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, alpha=0.1, label='Training Data (Synthetic-CST)')
    plt.plot(test_lens, preds, 'r-', lw=2, label='AI Prediction (MLP)')
    plt.axvline(x=163.5, color='green', alpha=0.3, label='CST Nominal')
    plt.title('AI-Powered S11 Optimizer (Neural Network Regression)')
    plt.xlabel('Arm Length (mm)')
    plt.ylabel('Predicted S11 (dB)')
    plt.legend()
    plt.grid(True)
    
    output_plot = os.path.join(PLOTS_DIR, 'ai_antenna_optimizer.png')
    plt.savefig(output_plot)
    print(f"Exported: {output_plot}")

if __name__ == "__main__":
    train_antenna_ai()
