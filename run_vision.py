#!/data/data/com.termux/files/usr/bin/env python3
import threading
from core.brain import VisionBrain
from core.auto_fix import AutoFix
from core.dashboard import run_dashboard
from core.feature_manager import FeatureManager
from core.audit import log
from core.voice import listen, speak

password = input("Enter Vision password: ")
brain = VisionBrain(password)
fixer = AutoFix()
features = FeatureManager()

log("VISION MAXIMUM LEVEL ADVANCED READY")

# Dashboard in background
dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
dashboard_thread.start()
log("Web Dashboard running at http://127.0.0.1:8080")

while True:
    cmd = input("VISION > ").strip()
    if cmd.lower() == "exit":
        log("Exiting Vision...")
        break

    if cmd.lower() == "dashboard":
        log("Dashboard running at http://127.0.0.1:8080")
        continue

    if cmd.lower() == "voice":
        speak("আমি শুনছি, বলুন কি করতে হবে")
        text = listen()
        reply = brain.think(text)
        speak(reply)
        continue

    # Auto-fix
    if "error" in cmd.lower() or "stuck" in cmd.lower():
        problem, fix = fixer.diagnose(cmd)
        if problem:
            fixer.propose(problem, fix)
        else:
            log("No known fix")
        continue

    # Auto-feature suggestion example
    if "add feature" in cmd.lower():
        feature_name = input("Enter feature name: ")
        feature_summary = input("Enter feature summary: ")
        features.propose(feature_name, feature_summary)
        continue

    # Normal chat
    reply = brain.think(cmd)
    print("VISION:", reply)
