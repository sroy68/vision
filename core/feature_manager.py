from core.audit import log

class FeatureManager:
    def __init__(self):
        self.installed = {}
        self.history = []

    def propose(self, name, summary):
        log(f"Feature proposed: {name} | {summary}")
        print(f"\nVISION FEATURE REQUEST\nFeature: {name}\nSummary: {summary}\nApprove? (YES/NO)")
        approve = input().strip().upper()
        if approve == "YES":
            self.install(name, summary)
            return True
        log(f"Feature {name} rejected by owner")
        return False

    def install(self, name, summary):
        self.installed[name] = summary
        self.history.append({"action": "install", "feature": name})
        log(f"Feature {name} installed")

    def undo(self, feature_name):
        if feature_name in self.installed:
            del self.installed[feature_name]
            self.history.append({"action": "undo", "feature": feature_name})
            log(f"Feature {feature_name} undone")
        else:
            log(f"No such feature to undo: {feature_name}")
