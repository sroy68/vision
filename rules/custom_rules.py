CUSTOM_RULES = [
  {
    "id": "XSS-REFLECTED",
    "pattern": "return f\"<h1>.*{",
    "context": ["flask", "route"],
    "impact": "Session hijack / defacement",
    "confidence": 0.85,
    "fix": "Use template auto-escape or html.escape()"
  },
  {
    "id": "SQLI-STRING",
    "pattern": "SELECT .* WHERE .*='",
    "context": ["sqlite", "execute"],
    "impact": "Auth bypass / data leak",
    "confidence": 0.9,
    "fix": "Parameterized queries"
  },
  {
    "id": "CMD-OS-SYSTEM",
    "pattern": "os.system",
    "context": ["user input"],
    "impact": "RCE",
    "confidence": 0.95,
    "fix": "subprocess.run(shell=False) + whitelist"
  }
]
