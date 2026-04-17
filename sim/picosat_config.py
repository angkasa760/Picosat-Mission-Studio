import os

# --- BASE CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM_DIR = os.path.join(BASE_DIR, 'sim')
WEB_DIR = os.path.join(BASE_DIR, 'web')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

# --- DATA PATHS ---
MISSION_DATA_PATH = os.path.join(DATA_DIR, 'mission_data.json')
LIVE_COORDS_PATH = os.path.join(WEB_DIR, 'live_coords.json')
PASSES_CSV_PATH = os.path.join(DATA_DIR, 'passes_jakarta.csv')
DE421_BSP_PATH = os.path.join(DATA_DIR, 'de421.bsp')
BEACON_WAV_PATH = os.path.join(DATA_DIR, 'picosat_beacon.wav')

# --- MISSION BASELINE ---
NORAD_ID = 66780 # FOSSASAT-2E24
TLE_URL = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={NORAD_ID}&FORMAT=TLE"
F_HZ_NOM = 437.2e6
G_TX_DBI_NOM = 2.06
S11_NOM = -20.5

# --- SYSTEM SETTINGS ---
DEBUG_MODE = False
LOG_LEVEL = "INFO"

def resolve_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

if __name__ == "__main__":
    print(f"Picosat Config Initialized. Base: {BASE_DIR}")
