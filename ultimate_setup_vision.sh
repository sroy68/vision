#!/data/data/com.termux/files/usr/bin/bash
# Ultimate Vision Setup Script for Termux
# One-command setup & auto-start
# Run: bash ultimate_setup_vision.sh

echo "=============================="
echo "Ultimate Vision Setup Starting"
echo "=============================="

# 1️⃣ Update Termux packages
pkg update -y
pkg upgrade -y

# 2️⃣ Install required packages
pkg install python git wget curl espeak -y

# 3️⃣ Install Python dependencies
pip install --upgrade pip
pip install pyttsx3 speechrecognition flask requests pyotp schedule

# 4️⃣ Clone / Pull Vision repository
VISION_DIR="$HOME/vision"
if [ -d "$VISION_DIR" ]; then
    echo "[INFO] Updating existing Vision repository..."
    cd "$VISION_DIR"
    git pull
else
    echo "[INFO] Cloning Vision repository..."
    git clone https://github.com/yourusername/vision.git "$VISION_DIR"
    cd "$VISION_DIR"
fi

# 5️⃣ Setup private config
CONFIG="$VISION_DIR/config_private.py"
if [ ! -f "$CONFIG" ]; then
    echo "[INFO] Creating config_private.py"
    cat <<EOL > $CONFIG
# chmod 600 config_private.py
OPENAI_API_KEY = ""
VISION_PASSWORD = "CHANGE_ME"
EOL
    chmod 600 $CONFIG
fi

# 6️⃣ Make main executable
chmod +x main.py

# 7️⃣ Create Termux auto-start script
SERVICE="$HOME/start_vision.sh"
cat <<EOL > $SERVICE
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd "$VISION_DIR"
# Launch Vision in background
nohup python main.py > vision.log 2>&1 &
echo "Vision launched in background. Dashboard: http://127.0.0.1:8080"
EOL
chmod +x $SERVICE

# 8️⃣ Create scheduled plugin updater script
SCHEDULE="$HOME/vision_plugin_update.sh"
cat <<EOL > $SCHEDULE
#!/data/data/com.termux/files/usr/bin/bash
cd "$VISION_DIR"
python -c "
from core.plugin_manager_full import FullPluginManager
pm = FullPluginManager()
pm.auto_install_trending(owner=True)
print('[INFO] Auto plugin update done')
"
EOL
chmod +x $SCHEDULE

# 9️⃣ Launch Vision for first time
echo "[INFO] Launching Vision..."
bash "$SERVICE"

echo "=============================="
echo "Ultimate Vision Setup Complete"
echo "Use 'bash start_vision.sh' to launch Vision anytime."
echo "Scheduled plugin updates: run 'bash vision_plugin_update.sh'"
echo "Web Dashboard: http://127.0.0.1:8080"
echo "=============================="
