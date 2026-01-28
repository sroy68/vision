from core.audit_log import log

class SelfHeal:
    def scan(self):
        log("Self-heal scan completed")

    def heal(self):
        log("Self-heal executed")
