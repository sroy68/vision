from core.audit import log

class RollbackManager:
    def __init__(self):
        self.history = []

    def save_state(self, state):
        self.history.append(state)

    def rollback(self):
        if not self.history:
            log("No rollback state available")
            return
        last = self.history.pop()
        log(f"Rollback executed: {last}")
