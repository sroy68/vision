#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd $HOME/vision
nohup python vision_runner.py > vision.log 2>&1 &
echo "Vision running in background. Dashboard: http://127.0.0.1:8080"
