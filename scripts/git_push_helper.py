import os
import subprocess

def run_git_ops():
    repo_path = r"C:\network_picosatellite\picosat"
    remote_url = "https://github.com/angkasa760/Picosat-Mission-Studio.git"
    
    os.chdir(repo_path)
    
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit: Picosat Mission Studio (Audited & Robust)"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", remote_url],
        ["git", "push", "-u", "origin", "main"]
    ]
    
    for cmd in commands:
        print(f"Executing: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error in {cmd[0]}: {e.stderr}")
            if "remote origin already exists" in e.stderr:
                subprocess.run(["git", "remote", "set-url", "origin", remote_url])
                continue
            break

if __name__ == "__main__":
    run_git_ops()
