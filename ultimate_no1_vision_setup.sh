#!/data/data/com.termux/files/usr/bin/bash
# World No.1 Vision AI setup

echo "=============================="
echo "Starting World No.1 Vision AI Setup"
echo "=============================="

pkg update -y
pkg upgrade -y
pkg install python git wget curl espeak -y

pip install --upgrade pip
pip install pyttsx3 speechrecognition flask requests pyotp schedule cryptography

VISION_DIR="$HOME/vision"
if [ ! -d "$VISION_DIR" ]; then
    git clone https://github.com/yourusername/vision.git "$VISION_DIR"
fi
cd "$VISION_DIR"

CONFIG="$VISION_DIR/config_private.py"
if [ ! -f "$CONFIG" ]; then
    cat <<EOL > $CONFIG
OPENAI_API_KEY = ""
VISION_PASSWORD = "CHANGE_ME"
EOL
    chmod 600 $CONFIG
fi

chmod +x vision_runner.py

# Termux background launch
SERVICE="$HOME/start_vision.sh"
cat <<EOL > $SERVICE
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd "$VISION_DIR"
nohup python vision_runner.py > vision.log 2>&1 &
echo "Vision World No.1 AI running"
EOL
chmod +x $SERVICE

OWNER_CONSOLE="$HOME/start_owner_console.sh"
cat <<EOL > $OWNER_CONSOLE
#!/data/data/com.termux/files/usr/bin/bash
cd "$VISION_DIR"
python core/owner_console.py
EOL
chmod +x $OWNER_CONSOLE

echo "[INFO] Setup Complete!"
echo "Use 'bash start_vision.sh' to launch Vision"
echo "Use 'bash start_owner_console.sh' for Owner Console"
echo "Dashboard: http://127.0.0.1:8080"
