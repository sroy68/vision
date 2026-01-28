from core.audit_log import log

class VisionBrain:
    def __init__(self, fm):
        self.fm = fm
        self.memory = []  # offline memory context

    # Basic offline AI reasoning
    def think(self, text):
        self.memory.append(f"User: {text}")
        # simple keyword matching + response generation
        text_lower = text.lower()

        # --- Feature detection ---
        feature_keywords = ["analyze", "monitor", "track", "detect", "usage", "battery", "notes"]
        if any(k in text_lower for k in feature_keywords):
            feature_name = "Auto Generated Feature"
            summary = f"Required to perform: {text}"
            self.fm.propose(feature_name, summary)
            return f"Feature '{feature_name}' requested based on your command."

        # --- Small offline responses ---
        if "hello" in text_lower or "hi" in text_lower:
            return "Hello! I am VISION, your AI assistant."
        if "status" in text_lower:
            return "All systems running. Security and features active."
        if "who are you" in text_lower:
            return "I am VISION, your controlled AI system."
        if "memory" in text_lower or "note" in text_lower:
            return f"I remember {len(self.memory)} previous interactions."

        # --- Default ---
        return "I understand. Tell me what you want to do next."

    def start(self):
        print("\nVISION READY TO CHAT (type 'exit' to quit)")
        while True:
            cmd = input("VISION > ").strip()
            if cmd.lower() == "exit":
                print("VISION shutting down chat.")
                break

            response = self.think(cmd)
            self.memory.append(f"Vision: {response}")
            log(f"[CHAT] User: {cmd}")
            log(f"[CHAT] Vision: {response}")
            print("VISION:", response)
