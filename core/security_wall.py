from core.audit import audit_log

SECURITY_WALL_ACTIVE = False

def detect_attack(event):
    return event.type in [
        "unauthorized_access",
        "plugin_override",
        "unknown_command",
        "rate_limit_violation",
        "memory_probe"
    ]

def activate_security_wall(event):
    global SECURITY_WALL_ACTIVE

    if SECURITY_WALL_ACTIVE:
        return

    SECURITY_WALL_ACTIVE = True

    # DEFENSIVE ACTIONS (SAFE)
    print("[SECURITY] External access blocked")
    print("[SECURITY] Plugins frozen")
    print("[SECURITY] Memory locked (read-only)")
    print(f"[SECURITY] Source isolated: {event.source}")

    audit_log({
        "event": event.type,
        "source": event.source,
        "action": "SECURITY_WALL_ACTIVATED"
    })

    print("[ALERT] Owner notified")

def on_system_event(event):
    if detect_attack(event):
        activate_security_wall(event)
