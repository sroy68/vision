#!/data/data/com.termux/files/usr/bin/bash
# ==========================================================
# Vision AI Full Setup + Test + Runner (Termux-ready)
# ==========================================================

VISION_DIR="$HOME/vision"
mkdir -p "$VISION_DIR"

echo "=============================="
echo "Starting Vision AI Full Setup"
echo "=============================="

# Step 1: Update Termux & install dependencies
pkg update -y
pkg upgrade -y
pkg install python git wget curl espeak -y

# Python packages (cryptography optional)
pip install --upgrade pip
pip install pyttsx3 speechrecognition flask requests schedule pyotp || echo "[WARNING] Some packages may fail, fallback enabled"

# Step 2: Ensure core directories
mkdir -p "$VISION_DIR/core"
mkdir -p "$VISION_DIR/memory"
mkdir -p "$VISION_DIR/plugins"
mkdir -p "$VISION_DIR/logs"

# Step 3: Create config_private.py if missing
CONFIG="$VISION_DIR/config_private.py"
if [ ! -f "$CONFIG" ]; then
cat <<EOL > $CONFIG
OPENAI_API_KEY = ""
VISION_PASSWORD = "CHANGE_ME"
EOL
chmod 600 $CONFIG
fi

# Step 4: Save memory.py (Termux-friendly)
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
                fernet = Fernet(self.key)
                json_data = json.dumps(self.data).encode()
                encrypted = fernet.encrypt(json_data)
                with open(self.path, "wb") as f:
                    f.write(encrypted)
            else:
                json_path = self.path.replace(".enc", ".json")
                with open(json_path, "w") as f:
                    json.dump(self.data, f)
        except Exception as e:
            print(f"[ERROR] Memory save failed: {e}")

    def load(self):
        try:
            if USE_CRYPTO and os.path.exists(self.path):
                fernet = Fernet(self.key)
                with open(self.path, "rb") as f:
                    decrypted = fernet.decrypt(f.read())
                    self.data = json.loads(decrypted)
            else:
                json_path = self.path.replace(".enc", ".json")
                if os.path.exists(json_path):
                    with open(json_path, "r") as f:
                        self.data = json.load(f)
        except Exception as e:
            print(f"[WARNING] Memory load failed, starting fresh: {e}")
            self.data = {"interactions": [], "errors": []}

    def log_interaction(self, query, response):
        self.data["interactions"].append({"query": query, "response": response, "time": time.time()})
        self.save()

    def log_error(self, error_msg):
        self.data["errors"].append({"error": error_msg, "time": time.time()})
        self.save()
EOL

# Step 5: Create minimal core/voice.py
cat <<'EOL' > "$VISION_DIR/core/voice.py"
def speak(text):
    print(f"[VOICE OUTPUT] {text}")

def listen():
    return input("[VOICE INPUT] ")
EOL

# Step 6: Create test_runner.py
cat <<'EOL' > "$VISION_DIR/test_runner.py"
from core.memory import Memory
from core.voice import speak, listen

mem = Memory("CHANGE_ME")
test_queries = ["Hello", "Cricket score", "Install plugin x"]
for q in test_queries:
    print("\nTEST QUERY:", q)
    resp = f"Simulated response for '{q}'"
    print("RESPONSE:", resp)
    mem.log_interaction(q, resp)

speak("Test voice output OK")
inp = "Test voice input"
print("[VOICE INPUT SIMULATED]:", inp)
print("\n✅ Minimal test finished successfully")
EOL

# Step 7: Run test_runner.py
echo "[INFO] Running minimal Vision AI test..."
python3 "$VISION_DIR/test_runner.py"

# Step 8: Create runner script
cat <<'EOL' > "$VISION_DIR/vision_runner.py"
#!/usr/bin/env python3
from core.memory import Memory
from core.voice import speak, listen
mem = Memory("CHANGE_ME")
print("VISION World No.1 AI ACTIVE")
while True:
    query = listen()
    if query.lower() in ["exit", "quit"]:
        mem.save()
        break
    resp = f"Simulated AI reply for '{query}'"
    print("VISION:", resp)
    speak(resp)
    mem.log_interaction(query, resp)
EOL
chmod +x "$VISION_DIR/vision_runner.py"

echo "=============================="
echo "✅ Vision AI setup complete"
echo "Run: ./vision_runner.py to start full Vision AI"
echo "=============================="
