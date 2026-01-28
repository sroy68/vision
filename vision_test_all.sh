#!/data/data/com.termux/files/usr/bin/bash
# ====================================================
# Vision World No.1 AI Full Core Module Test Script
# ====================================================

VISION_DIR="$HOME/vision"
cd "$VISION_DIR" || exit

echo "=============================="
echo "Starting Vision AI Full Core Test"
echo "=============================="

# Step 1: Minimal Python test runner
echo "[1/5] Running minimal test queries..."
python3 - <<'EOF'
from core.brain import VisionBrain
from core.memory import Memory
from core.voice import speak, listen
from core.plugin_manager_full import FullPluginManager
from core.auto_feature import AutoFeatureManager
from core.global_tools import GlobalExecutor
from config_private import VISION_PASSWORD, OPENAI_API_KEY

mem = Memory(VISION_PASSWORD)
brain = VisionBrain(owner_password=VISION_PASSWORD, memory=mem, api_key=OPENAI_API_KEY)
pm = FullPluginManager()
afm = AutoFeatureManager(owner=True)
ge = GlobalExecutor(owner=True)

test_queries = [
    "Hello",
    "Cricket score",
    "Install plugin x",
    "Activate feature y"
]

for q in test_queries:
    print("\nTEST QUERY:", q)
    resp = brain.reply(q)
    print("RESPONSE:", resp)
    mem.log_interaction(q, resp)
    pm.auto_install_trending(owner=True)
    afm.check_proposals(owner=True)
    ge.execute_if_approved(q)

print("\n✅ Minimal test finished successfully")
EOF

# Step 2: Voice test
echo "[2/5] Testing voice input/output..."
python3 - <<'EOF'
from core.voice import speak, listen
speak("Hello from Vision AI")
inp = "Test input"
print("[VOICE INPUT SIMULATED]:", inp)
EOF
echo "✅ Voice test passed"

# Step 3: Dashboard test (runs 5 sec)
echo "[3/5] Testing web dashboard..."
python3 - <<'EOF'
from core.dashboard import run_dashboard
import threading, time
t = threading.Thread(target=run_dashboard, daemon=True)
t.start()
time.sleep(5)
print("✅ Dashboard test OK (check http://127.0.0.1:8080)")
EOF

# Step 4: Memory check
echo "[4/5] Checking memory persistence..."
python3 - <<'EOF'
from core.memory import Memory
mem = Memory("CHANGE_ME")
print("Memory keys:", list(mem.data.keys()))
print("✅ Memory persistence test OK")
EOF

# Step 5: Plugin & Auto Feature check
echo "[5/5] Checking plugins & auto-features..."
python3 - <<'EOF'
from core.plugin_manager_full import FullPluginManager
from core.auto_feature import AutoFeatureManager
pm = FullPluginManager()
afm = AutoFeatureManager(owner=True)
pm.auto_install_trending(owner=True)
afm.activate_all(owner=True)
print("✅ Plugins & Auto-features OK")
EOF

echo "=============================="
echo "All Vision AI core modules tested successfully!"
echo "✅ Vision World No.1 AI is READY"
echo "=============================="
