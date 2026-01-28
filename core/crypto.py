import os
from hashlib import pbkdf2_hmac
from base64 import urlsafe_b64encode

SALT_FILE = ".vision_salt"

def derive_key(password: str) -> bytes:
    if not os.path.exists(SALT_FILE):
        open(SALT_FILE, "wb").write(os.urandom(16))

    salt = open(SALT_FILE, "rb").read()
    key = pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200_000,
        dklen=32
    )
    return key
