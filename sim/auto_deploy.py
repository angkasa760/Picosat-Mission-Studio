import os
import subprocess
import datetime

def auto_deploy(message=None):
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_path)
    
    if not message:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Synchronized Update: {timestamp} (via Antigravity AI)"
    
    print(f"--- AUTO-DEPLOY STARTING in {repo_path} ---")
    
    try:
        # Check if it's a git repo
        if not os.path.exists(os.path.join(repo_path, ".git")):
            print("Initializing Git Repository...")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/angkasa760/Picosat-Mission-Studio.git"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)

        # Sync
        print("Staging changes...")
        subprocess.run(["git", "add", "."], check=True)
        
        # Check for changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
        if not status:
            print("No changes to deploy.")
            return

        print("Committing changes...")
        subprocess.run(["git", "commit", "-m", message], check=True)
        
        print("Pushing to GitHub...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print(f"--- SUCCESS: Pushed to 'main' at {datetime.datetime.now()} ---")
        
    except subprocess.CalledProcessError as e:
        print(f"Deployment failed: {e}")
    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    auto_deploy()
