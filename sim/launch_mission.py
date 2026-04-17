import subprocess
import sys
import os
import time
import webbrowser
import http.server
import socketserver
import threading
import socket

# --- MISSION CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, 'web')
PORT = 8000

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_server():
    os.chdir(BASE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"[SERVER] Mission Control Lab active at http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"[SERVER] Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("   PIN-UHF PICOSATELLITE MISSION BOOTSTRAPPER")
    print("="*50 + "\n")

    # 1. Verification of Dependencies
    print("[1/4] Checking System Dependencies...")
    libs = ["customtkinter", "skyfield", "requests", "pandas", "numpy", "matplotlib"]
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            print(f"Installing missing library: {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

    # 2. Start Web Server
    print("[2/4] Initializing Local Data Server...")
    if not is_port_in_use(PORT):
        threading.Thread(target=start_server, daemon=True).start()
        time.sleep(2)
    else:
        print(f"Port {PORT} already active. Proceeding...")

    # 3. Launch Dashboards
    print("[3/4] Launching Cinematic Mission Visuals...")
    webbrowser.open(f"http://localhost:{PORT}/web/orbit.html")
    
    # 4. Launch Desktop Control GUI
    print("[4/4] Starting Desktop Ground Control GUI...")
    gui_script = os.path.join(BASE_DIR, 'sim', 'ground_control.py')
    
    # Run GUI in a new process so it doesn't block
    subprocess.Popen([sys.executable, gui_script], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)

    print("\n" + "="*50)
    print("   MISSION SUCCESS: ALL SYSTEMS NOMINAL")
    print("   Please keep this terminal window open.")
    print("="*50 + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMission Terminated by User.")
