from core.audit_log import log

class Approval:
    def ask(self, name, summary, session_unlocked=False):
        if session_unlocked:
            log(f"Feature auto-approved: {name}")
            return True

        print("\n======================")
        print("VISION FEATURE REQUEST")
        print("Feature :", name)
        print("Summary :", summary)
        print("======================")
        decision = input("Approve? (YES/NO): ").strip().upper()
        log(f"OWNER decision {name}: {decision}")
        return decision == "YES"
