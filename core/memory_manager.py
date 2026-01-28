import json, os, base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from core.audit_log import log
from config import OWNER_PASSWORD

MEMORY_FILE = "vision_memory.enc"

class MemoryManager:
    def __init__(self):
        self.key = OWNER_PASSWORD.encode('utf-8').ljust(32, b'0')  # AES-256 key
        self.memory = {"chat": [], "features": []}
        self.load()

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, data):
        raw = base64.b64decode(data)
        nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            f.write(self.encrypt(json.dumps(self.memory)))
        log("[MEMORY SAVED]")

    def load(self):
        if not os.path.exists(MEMORY_FILE):
            return
        try:
            with open(MEMORY_FILE) as f:
                self.memory = json.loads(self.decrypt(f.read()))
            log("[MEMORY LOADED]")
        except:
            log("[MEMORY LOAD FAILED]")
            self.memory = {"chat": [], "features": []}

    def add_chat(self, user, vision):
        self.memory["chat"].append({"user": user, "vision": vision})
        self.save()

    def add_feature(self, feature, summary):
        self.memory["features"].append({"feature": feature, "summary": summary})
        self.save()
