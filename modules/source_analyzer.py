import re

class SourceAnalyzer:
    def analyze(self, code: str):
        findings = []

        # 1. XSS risk (analysis only)
        if re.search(r"innerHTML\s*=", code):
            findings.append({
                "issue": "Possible XSS",
                "where": "Usage of innerHTML",
                "impact": "User-controlled input হলে script inject হতে পারে",
                "fix": "textContent ব্যবহার করো বা proper output encoding"
            })

        # 2. SQL Injection risk (analysis only)
        if re.search(r"SELECT .* \+ .*", code, re.I):
            findings.append({
                "issue": "Possible SQL Injection",
                "where": "String concatenation in SQL query",
                "impact": "Attacker query modify করতে পারে",
                "fix": "Prepared statements / parameterized queries ব্যবহার করো"
            })

        # 3. Hardcoded secret
        if re.search(r"API_KEY|SECRET|PASSWORD\s*=\s*['\"]", code):
            findings.append({
                "issue": "Hardcoded Secret",
                "where": "Source code",
                "impact": "Key leak হলে full compromise",
                "fix": "Environment variable / secret manager ব্যবহার করো"
            })

        return findings
