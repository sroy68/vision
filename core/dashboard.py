from flask import Flask
app = Flask("VisionDashboard")

@app.route("/")
def home():
    return "<h1>Vision World No.1 AI Dashboard</h1><p>Status: ACTIVE</p>"

def run_dashboard():
    app.run(host="0.0.0.0", port=8080)
