import os
import shutil

def reorganize():
    base_dir = r"C:\network_picosatellite\picosat"
    
    # Target Directories
    dirs = ["data", "models", "plots", "scripts"]
    for d in dirs:
        path = os.path.join(base_dir, d)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")

    # File Mappings (Source -> Destination Folder)
    mappings = {
        "data": [
            "mission_data.json",
            "passes_jakarta.csv",
            "de421.bsp",
            "picosat_beacon.wav",
            "passes_jakarta.csv"
        ],
        "models": [
            "antenna_model.pkl",
            "scaler_x.pkl",
            "scaler_y.pkl"
        ],
        "scripts": [
            "git_push_helper.py",
            "move_banner.py",
            "git_push_helper.py"
        ],
        "plots": [
            "ai_antenna_optimizer.png",
            "doppler_analysis.png",
            "link_budget_analysis.png",
            "lora_sim_performance.png",
            "mission_reliability_plot.png",
            "power_cycle_analysis.png",
            "rf_propagation.gif",
            "sensitivity_analysis.png",
            "thermal_analysis.png",
            "vibration_analysis.png",
            "vna_hardware_comparison.png"
        ]
    }

    # Execute Moves
    for folder, files in mappings.items():
        dest_dir = os.path.join(base_dir, folder)
        for f in files:
            src_path = os.path.join(base_dir, f)
            dest_path = os.path.join(dest_dir, f)
            if os.path.exists(src_path):
                try:
                    shutil.move(src_path, dest_path)
                    print(f"Moved: {f} -> {folder}/")
                except Exception as e:
                    print(f"Error moving {f}: {e}")
            else:
                # Check maybe it's already there?
                if os.path.exists(dest_path):
                    print(f"Already in place: {f}")
                else:
                    print(f"File not found: {f}")

    print("\n--- REORGANIZATION COMPLETE ---")

if __name__ == "__main__":
    reorganize()
