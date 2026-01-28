from core.brain import VisionBrain
from dashboard.app import run_dashboard
import threading

brain = VisionBrain()

print("[VISION] System Ready")

# start dashboard in background
threading.Thread(target=run_dashboard, daemon=True).start()

while True:
    try:
        user_input = input("VISION > ")
        print("VISION:", brain.handle_input(user_input))
    except KeyboardInterrupt:
        print("\n[VISION] Shutdown")
        break
