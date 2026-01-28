# ctf/app.py
from flask import Flask, request
import sqlite3, os

app = Flask(__name__)

@app.route("/xss")
def xss():
    q = request.args.get("q", "")
    return f"<h1>Search: {q}</h1>"   # INTENTIONAL XSS (training)

@app.route("/sqli")
def sqli():
    user = request.args.get("user","")
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users(name TEXT);")
    db.execute("INSERT INTO users VALUES ('admin')")
    q = f"SELECT * FROM users WHERE name='{user}'"  # INTENTIONAL SQLi
    return str(db.execute(q).fetchall())

@app.route("/cmd")
def cmd():
    c = request.args.get("c","")
    os.system(c)  # INTENTIONAL (do NOT deploy)
    return "ok"

if __name__ == "__main__":
    app.run(port=5005)
