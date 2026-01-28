from flask import Flask
from core.security_wall import SECURITY_WALL_ACTIVE
from core.audit import get_audit_log

app = Flask(__name__)

@app.route("/")
def index():
    status = "ACTIVE" if SECURITY_WALL_ACTIVE else "NORMAL"
    logs = get_audit_log()

    html = f"""
    <h1>VISION DASHBOARD</h1>
    <h2>Security Wall: {status}</h2>
    <pre>{logs}</pre>
    """
    return html

def run_dashboard():
    app.run(host="127.0.0.1", port=8080)
