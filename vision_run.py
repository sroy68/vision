import os
import re
import argparse
import requests
from urllib.parse import urlparse
from datetime import datetime

SUPPORTED_EXT = (".py", ".js", ".php", ".java")
REPORT_FILE = "vision_report.txt"

# ---------------- URL FETCH ----------------
def fetch_url(url):
    print("[VISION] Fetching public URL (GET only)...")
    r = requests.get(
        url,
        timeout=10,
        headers={"User-Agent": "Vision-BugBounty-Analyzer"}
    )
    return r.text, r.headers

# ---------------- URL ANALYSIS ----------------
def analyze_url(html, headers):
    issues = []

    if "innerHTML" in html:
        issues.append((
            "DOM XSS Risk",
            "innerHTML",
            "User input থাকলে script inject হতে পারে",
            "textContent বা proper output encoding ব্যবহার করো"
        ))

    if re.search(r"eval\(|document\.write\(", html):
        issues.append((
            "Dangerous JS Function",
            "eval / document.write",
            "DOM-based XSS সম্ভব",
            "এই function গুলো বাদ দাও"
        ))

    if "Content-Security-Policy" not in headers:
        issues.append((
            "Missing CSP",
            "HTTP Header",
            "XSS impact অনেক বেড়ে যায়",
            "Strict Content-Security-Policy যোগ করো"
        ))

    if "X-Frame-Options" not in headers:
        issues.append((
            "Missing X-Frame-Options",
            "HTTP Header",
            "Clickjacking সম্ভব",
            "X-Frame-Options: DENY বা SAMEORIGIN সেট করো"
        ))

    if "Strict-Transport-Security" not in headers:
        issues.append((
            "Missing HSTS",
            "HTTP Header",
            "MITM / SSL downgrade risk",
            "Strict-Transport-Security header যোগ করো"
        ))

    return issues

# ---------------- SOURCE ANALYSIS ----------------
def analyze_code(code, filename):
    issues = []

    if re.search(r"SELECT\s+.*\+\s*", code, re.I):
        issues.append((
            "Possible SQL Injection",
            filename,
            "User input দিয়ে SQL query manipulate করা সম্ভব",
            "Prepared statements / parameterized query ব্যবহার করো"
        ))

    if "pickle.loads" in code:
        issues.append((
            "Insecure Deserialization",
            filename,
            "Remote Code Execution (RCE) হতে পারে",
            "JSON বা safe serialization ব্যবহার করো"
        ))

    if re.search(r"os\.system|subprocess\.Popen", code):
        issues.append((
            "Command Injection Risk",
            filename,
            "OS command execute হতে পারে",
            "subprocess.run(shell=False) + strict whitelist ব্যবহার করো"
        ))

    if re.search(r"password\s*=\s*['\"]", code, re.I):
        issues.append((
            "Hardcoded Secret",
            filename,
            "Credential leak হওয়ার ঝুঁকি",
            "Environment variable বা secret manager ব্যবহার করো"
        ))

    return issues

def scan_source(path):
    all_issues = []

    if os.path.isfile(path):
        with open(path, "r", errors="ignore") as f:
            all_issues.extend(analyze_code(f.read(), path))

    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(SUPPORTED_EXT):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", errors="ignore") as f:
                            all_issues.extend(analyze_code(f.read(), full_path))
                    except:
                        pass
    else:
        print("❌ Invalid source path")

    return all_issues

# ---------------- REPORT GENERATION ----------------
def generate_report(target, issues):
    with open(REPORT_FILE, "w") as f:
        f.write("VISION BUG BOUNTY SECURITY REPORT\n")
        f.write("=" * 45 + "\n")
        f.write(f"Target : {target}\n")
        f.write(f"Date   : {datetime.now()}\n\n")

        if not issues:
            f.write("✅ No security issues found.\n")
        else:
            for i, issue in enumerate(issues, 1):
                f.write(f"[{i}] Problem : {issue[0]}\n")
                f.write(f"    Where  : {issue[1]}\n")
                f.write(f"    Impact : {issue[2]}\n")
                f.write(f"    Fix    : {issue[3]}\n\n")

        f.write("Note: Analysis-only. No exploitation performed.\n")

    print(f"[VISION] Report generated → {REPORT_FILE}")

# ---------------- MAIN ----------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Live website URL")
    parser.add_argument("--source", help="Source file or folder path")
    args = parser.parse_args()

    all_issues = []

    if not args.url and not args.source:
        print("Usage:")
        print("  python vision_run.py --url https://site.com")
        print("  python vision_run.py --source app.py")
        print("  python vision_run.py --url https://site.com --source ./project/")
        return

    if args.url:
        parsed = urlparse(args.url)
        if parsed.scheme.startswith("http"):
            html, headers = fetch_url(args.url)
            all_issues.extend(analyze_url(html, headers))
        else:
            print("❌ Invalid URL")

    if args.source:
        all_issues.extend(scan_source(args.source))

    target = args.url if args.url else args.source
    print("[VISION] Analysis finished, generating report...")
    generate_report(target, all_issues)

    print("🔒 Analysis-only | No exploit | Bug-bounty safe")

if __name__ == "__main__":
    main()
