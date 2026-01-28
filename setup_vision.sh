#!/data/data/com.termux/files/usr/bin/bash
# Termux Ultimate Vision Setup Script
# Run: bash setup_vision.sh

echo "=============================="
echo "Vision Ultimate Setup Starting"
echo "=============================="

# 1️⃣ Update Termux packages
pkg update -y
pkg upgrade -y

# 2️⃣ Install required packages
pkg install python git wget curl espeak -y

# 3️⃣ Install Python dependencies
pip install --upgrade pip
pip install pyttsx3 speechrecognition flask requests pyotp

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

# 7️⃣ Create Termux service script for auto-start
SERVICE="$HOME/start_vision.sh"
cat <<EOL > $SERVICE
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd "$VISION_DIR"
python main.py
EOL
chmod +x $SERVICE

# 8️⃣ Launch Vision for first time
echo "[INFO] Launching Vision..."
bash "$SERVICE" &

echo "=============================="
echo "Vision Setup Complete"
echo "Use 'bash start_vision.sh' to launch Vision anytime."
echo "Web Dashboard: http://127.0.0.1:8080"
echo "=============================="
