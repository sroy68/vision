import subprocess
from core.rollback import RollbackManager
from core.history import FixHistory
from core.explain import explain_decision

class AutoFix:
    def __init__(self):
        self.rb = RollbackManager()
        self.history = FixHistory()

    def diagnose(self, text):
        if "pydantic" in text or "wheel" in text:
            return "Dependency build stuck", \
                   "pip uninstall openai pydantic -y && pip install openai<2 pydantic<2"
        return None, None

    def propose(self, problem, fix):
        print(explain_decision(problem, fix))
        if input("Approve auto-fix? (YES/NO): ").upper() == "YES":
            self.apply(fix, problem)

    def apply(self, fix, problem):
        self.rb.save_state("before-fix")
        self.history.add(problem, fix)
        subprocess.call(fix, shell=True)
