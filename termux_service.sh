#!/data/data/com.termux/files/usr/bin/bash
# Termux service for VISION auto-start

# wake lock
termux-wake-lock

# move to vision dir
cd /data/data/com.termux/files/home/vision

# run VISION in background
nohup python main.py &> vision.log &
