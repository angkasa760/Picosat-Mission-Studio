import sys
import os

# --- PATH INJECTION FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

import customtkinter as ctk
import time
import json

from sim.picosat_config import MISSION_DATA_PATH, LIVE_COORDS_PATH

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MissionControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("PIN-UHF Ground Station - REAL-TIME MISSION OPS")
        self.geometry("1100x650")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -- Sidebar --
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.sidebar, text="PIN-UHF Control", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.clock_label = ctk.CTkLabel(self.sidebar, text="UTC: 00:00:00", font=ctk.CTkFont(size=14))
        self.clock_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.status_sun = ctk.CTkLabel(self.sidebar, text="SUNLIT: ---", text_color="#ffd700")
        self.status_sun.grid(row=2, column=0, padx=20, pady=10)

        # -- Main Content --
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.telemetry_labels = {}
        self.create_telemetry_box("Link Margin", "---", 0, 0, "#00ff88")
        self.create_telemetry_box("Battery SoC", "---", 0, 1, "#00f2ff")
        self.create_telemetry_box("Altitude / Ground", "---", 1, 0, "#8892b0")
        self.create_telemetry_box("Thermal Temp", "---", 1, 1, "#ff5555")
        
        self.console = ctk.CTkTextbox(self.main_frame, height=220)
        self.console.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.log("Mission Ops Center Active. Connecting to Tracker physics engine...")

        self.update_clock()
        self.poll_realtime_data()

    def create_telemetry_box(self, label, value, row, col, color):
        box = ctk.CTkFrame(self.main_frame, fg_color="#1a222d", corner_radius=15, border_width=1, border_color="#2e3a4e")
        box.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        l_label = ctk.CTkLabel(box, text=label.upper(), font=ctk.CTkFont(size=11, weight="bold"))
        l_label.pack(pady=(15, 0))
        
        l_val = ctk.CTkLabel(box, text=value, text_color=color, font=ctk.CTkFont(family="Consolas", size=32, weight="bold"))
        l_val.pack(pady=15)
        
        self.telemetry_labels[label] = l_val

    def poll_realtime_data(self):
        try:
            if os.path.exists(LIVE_COORDS_PATH):
                with open(LIVE_COORDS_PATH, 'r') as f:
                    data = json.load(f)
                
                # 1. Update Display avec REAL Physics
                margin = data.get('live_link_margin', -99.9)
                self.telemetry_labels["Link Margin"].configure(
                    text=f"{margin:+.1f} dB" if margin > -90 else "LOS"
                )
                
                soc = data.get('battery_soc', 0.0)
                self.telemetry_labels["Battery SoC"].configure(text=f"{soc:.1f} %")
                
                alt = data.get('alt', 0)
                lat, lon = data.get('lat', 0), data.get('lon', 0)
                self.telemetry_labels["Altitude / Ground"].configure(text=f"{alt}km | {lat}N")
                
                temp = data.get('temp_c', 0.0)
                self.telemetry_labels["Thermal Temp"].configure(text=f"{temp:+.1f} °C")
                
                sunlit = data.get('is_sunlit', True)
                self.status_sun.configure(text=f"SUNLIT: {'YES' if sunlit else 'ECLIPSE'}")
        except:
            pass
        self.after(1000, self.poll_realtime_data)

    def log(self, message):
        t_str = time.strftime("[%H:%M:%S] ")
        self.console.insert("end", t_str + message + "\n")
        self.console.see("end")

    def update_clock(self):
        utc_t = time.strftime("%H:%M:%S UTC", time.gmtime())
        self.clock_label.configure(text=utc_t)
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    try:
        app = MissionControlApp()
        app.mainloop()
    except Exception as e:
        print(f"Skipping GUI Mainloop (No Display): {e}")
