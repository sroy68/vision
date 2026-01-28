import pyotp

SECRET = pyotp.random_base32()
_totp = pyotp.TOTP(SECRET)

def show_qr():
    print("Add this secret to your Authenticator app:")
    print(SECRET)

def verify_totp(code):
    return _totp.verify(code, valid_window=10)  # ~5 minutes tolerance
