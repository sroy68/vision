#!/data/data/com.termux/files/usr/bin/bash
# =====================================================
# Vision World No.1 AI – Full Termux Setup + Runner
# =====================================================

VISION_DIR="$HOME/vision"
mkdir -p "$VISION_DIR"/{core,memory,plugins,logs}

echo "=============================="
echo "Starting Vision World No.1 AI Setup"
echo "=============================="

# Step 1: Update Termux and install base packages
pkg update -y
pkg upgrade -y
pkg install python git wget curl espeak -y

# Step 2: Python dependencies (cryptography optional)
pip install --upgrade pip
pip install pyttsx3 speechrecognition flask requests schedule pyotp || echo "[WARNING] Some packages may fail, fallback enabled"

# Step 3: Config (owner password + OpenAI key)
CONFIG="$VISION_DIR/config_private.py"
if [ ! -f "$CONFIG" ]; then
cat <<EOL > $CONFIG
OPENAI_API_KEY = ""
VISION_PASSWORD = "CHANGE_ME"
EOL
chmod 600 $CONFIG
fi

# Step 4: Memory (Termux-friendly fallback)
cat <<'EOL' > "$VISION_DIR/core/memory.py"
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
EOL

# Step 5: Voice interface
cat <<'EOL' > "$VISION_DIR/core/voice.py"
def speak(text):
    print(f"[VOICE OUTPUT] {text}")
def listen():
    return input("[VOICE INPUT] ")
EOL

# Step 6: Minimal Brain (Hybrid Reasoning placeholder)
cat <<'EOL' > "$VISION_DIR/core/brain.py"
from core.memory import Memory
class VisionBrain:
    def __init__(self, owner_password, memory, api_key=""):
        self.owner_password = owner_password
        self.memory = memory
        self.api_key = api_key
    def reply(self, query):
        # Simulated hybrid reasoning (offline fallback)
        if "google" in query.lower():
            return "Google একটি search engine, তথ্য খোঁজার জন্য ব্যবহার হয়।"
        elif "cricket" in query.lower():
            return "Score update: Team A 120/3 (Simulated)"
        else:
            return f"Simulated AI reply for '{query}'"
EOL

# Step 7: Minimal Plugin & AutoFeature (simulated)
cat <<'EOL' > "$VISION_DIR/core/plugin_manager_full.py"
class FullPluginManager:
    def auto_install_trending(self, owner=True):
        if owner: print("[PLUGIN] Trending plugins checked and installed (simulated)")
class AutoFeatureManager:
    def __init__(self, owner=False):
        self.owner=owner
    def activate_all(self, owner=True):
        if owner: print("[AUTO-FEATURE] All features activated (simulated)")
EOL

# Step 8: Vision AI Runner
cat <<'EOL' > "$VISION_DIR/vision_runner.py"
#!/usr/bin/env python3
from core.memory import Memory
from core.voice import speak, listen
from core.brain import VisionBrain
from core.plugin_manager_full import FullPluginManager, AutoFeatureManager

mem = Memory("CHANGE_ME")
brain = VisionBrain(owner_password="CHANGE_ME", memory=mem)
pm = FullPluginManager()
afm = AutoFeatureManager(owner=True)

print("VISION World No.1 AI ACTIVE (Type 'exit' to quit)")
while True:
    query = listen()
    if query.lower() in ["exit","quit"]:
        mem.save()
        break
    resp = brain.reply(query)
    print("VISION:", resp)
    speak(resp)
    mem.log_interaction(query, resp)
    pm.auto_install_trending(owner=True)
    afm.activate_all(owner=True)
EOL
chmod +x "$VISION_DIR/vision_runner.py"

echo "=============================="
echo "✅ Full Vision World No.1 AI setup complete!"
echo "Run: $VISION_DIR/vision_runner.py to start AI"
echo "=============================="
