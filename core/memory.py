import os, json, time, hashlib, base64
try:
    from cryptography.fernet import Fernet
    USE_CRYPTO = True
except ImportError:
    USE_CRYPTO = False
    print("[WARNING] cryptography not found. Memory will be saved as plain JSON.")

class Memory:
    def __init__(self, password, path=None):
        self.password = password.encode()
        self.path = path or os.path.expanduser("~/vision/memory/memory.enc")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.data = {"interactions": [], "errors": []}
        self.key = self.derive_key(password)
        self.load()
    def derive_key(self, password):
        hashed = hashlib.sha256(password).digest()
        return base64.urlsafe_b64encode(hashed)
    def save(self):
        try:
            if USE_CRYPTO:
                from cryptography.fernet import Fernet
                fernet = Fernet(self.key)
                encrypted = fernet.encrypt(json.dumps(self.data).encode())
                with open(self.path, "wb") as f:
                    f.write(encrypted)
            else:
                json_path = self.path.replace(".enc",".json")
                with open(json_path,"w") as f:
                    json.dump(self.data,f)
        except Exception as e:
            print(f"[ERROR] Memory save failed: {e}")
    def load(self):
        try:
            if USE_CRYPTO and os.path.exists(self.path):
                from cryptography.fernet import Fernet
                fernet = Fernet(self.key)
                with open(self.path,"rb") as f:
                    self.data = json.loads(fernet.decrypt(f.read()))
            else:
                json_path = self.path.replace(".enc",".json")
                if os.path.exists(json_path):
                    with open(json_path,"r") as f:
                        self.data = json.load(f)
        except Exception as e:
            print(f"[WARNING] Memory load failed, starting fresh: {e}")
            self.data={"interactions": [],"errors":[]}
    def log_interaction(self, query, response):
        self.data["interactions"].append({"query":query,"response":response,"time":time.time()})
        self.save()
    def log_error(self,error_msg):
        self.data["errors"].append({"error":error_msg,"time":time.time()})
        self.save()
