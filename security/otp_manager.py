import pyotp
import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD

def send_email_otp(email):
    otp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    code = otp.now()

    msg = MIMEText(f"Your VISION OTP: {code}")
    msg["Subject"] = "VISION OTP"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email

    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(SMTP_EMAIL, SMTP_PASSWORD)
    s.send_message(msg)
    s.quit()

    return code

def send_alert_email(subject, body, emails):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL

    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(SMTP_EMAIL, SMTP_PASSWORD)

    for e in emails:
        msg["To"] = e
        s.send_message(msg)
    s.quit()
