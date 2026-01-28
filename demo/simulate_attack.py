from core.brain import VisionBrain

brain = VisionBrain()

print("[DEMO] Simulating attack event...")
brain.system_event("unauthorized_access", "unknown_ip")
