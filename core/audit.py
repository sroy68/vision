import time

AUDIT_LOG = []

def audit_log(entry: dict):
    entry["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    AUDIT_LOG.append(entry)

def get_audit_log():
    return AUDIT_LOG
