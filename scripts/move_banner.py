import shutil
import os

source = r"C:\Users\GRSS NATAWARA\.gemini\antigravity\brain\35c777b3-7797-4a9e-a6b4-52ab2b40bbf1\picosat_hero_banner_1776418071912.png"
dest = r"C:\network_picosatellite\picosat\docs\banner.png"

try:
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    shutil.copy(source, dest)
    print(f"Success: Copied banner to {dest}")
except Exception as e:
    print(f"Error: {e}")
