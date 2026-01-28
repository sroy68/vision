import time
from collections import defaultdict
from core.audit_log import log
from security.otp_manager import send_alert_email
from config import FAILED_LIMIT, AUTO_UNLOCK_SECONDS, ALERT_EMAILS

class AntiHack:
    def __init__(self):
        self.failed = defaultdict(int)
        self.locked = False
        self.lock_time = None

    def fail(self, src="local"):
        self.failed[src] += 1
        log(f"[FAIL] {src} -> {self.failed[src]}")
        if self.failed[src] >= FAILED_LIMIT:
            self.lock(f"Brute force from {src}")

    def lock(self, reason):
        if self.locked:
            return
        self.locked = True
        self.lock_time = time.time()
        log("[SYSTEM LOCKED]")
        send_alert_email(
            "VISION SECURITY ALERT",
            f"LOCKED\nReason: {reason}",
            ALERT_EMAILS
        )

    def auto_unlock(self):
        if self.locked and time.time() - self.lock_time >= AUTO_UNLOCK_SECONDS:
            self.locked = False
            self.failed.clear()
            log("[AUTO UNLOCKED]")

    def live_monitor(self):
        log("[ANTI-HACK STARTED]")
        while True:
            self.auto_unlock()
            time.sleep(5)
