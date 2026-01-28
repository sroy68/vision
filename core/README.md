# VISION AI - Termux & GitHub-ready

## Features
- Hybrid Brain (online GPT + offline reasoning)
- Owner-only auto-feature management
- Encrypted persistent memory
- Auto-fix + rollback
- Web dashboard (localhost)
- Terminal-based voice placeholder
- Bengali + English explanation
- Live logs + history

## Run Instructions

1. Make executable:
   chmod +x main.py

2. Run:
   python main.py

3. Optional background run:
   termux-wake-lock
   nohup python main.py &

4. Stop background:
   ps aux | grep main.py
   kill <pid>

## Notes
- Owner password required for encrypted memory
- Voice is terminal-based, crash-free in Termux
- Web dashboard available at: http://127.0.0.1:8080
