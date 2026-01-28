from core.audit import log

class FixHistory:
    def __init__(self):
        self.history = []

    def add(self, problem, fix):
        self.history.append({"problem": problem, "fix": fix})

    def show(self):
        for i, h in enumerate(self.history):
            print(f"{i}: {h['problem']} → {h['fix']}")

    def undo(self, index):
        if index < 0 or index >= len(self.history):
            log("Invalid undo index")
            return
        h = self.history[index]
        log(f"Undo requested for: {h}")
