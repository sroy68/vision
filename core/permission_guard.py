from config import OWNER_PHONE, OWNER_EMAIL, OWNER_PASSWORD
from security.otp_manager import send_email_otp
from core.audit_log import log

class PermissionGuard:
    def __init__(self):
        self.session_unlocked = False

    def authenticate(self):
        print("[SECURITY] Sending EMAIL OTP...")
        otp = send_email_otp(OWNER_EMAIL)
        log("[EMAIL OTP SENT]")

        print(f"Phone: {OWNER_PHONE}")
        print(f"Email: {OWNER_EMAIL}")

        user_otp = input("Email OTP: ")
        pwd = input("Password: ")

        if user_otp == otp and pwd == OWNER_PASSWORD:
            self.session_unlocked = True
            log("[AUTH SUCCESS]")
            return True

        log("[AUTH FAILED]")
        return False

    def require(self):
        if not self.session_unlocked:
            raise PermissionError("OWNER AUTH FAILED")
