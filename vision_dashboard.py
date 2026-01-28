from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<h1>🧠 Vision Security Dashboard</h1>
<pre>{{content}}</pre>
"""

@app.route("/")
def index():
    if os.path.exists("vision_report.txt"):
        data = open("vision_report.txt").read()
    else:
        data = "No report generated yet."
    return render_template_string(HTML, content=data)

if __name__ == "__main__":
    app.run(port=8080)
