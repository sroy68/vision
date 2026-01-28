from modules.source_analyzer import SourceAnalyzer

VULNERABLE_CODE = """
user = input()
query = "SELECT * FROM users WHERE name = '" + user + "'"
"""

def start_ctf():
    print("=== CTF TRAINING MODE (OFFLINE) ===")
    analyzer = SourceAnalyzer()
    result = analyzer.analyze(VULNERABLE_CODE)

    for r in result:
        print("\n[ISSUE FOUND]")
        print("Type :", r["issue"])
        print("Impact :", r["impact"])
        print("Fix :", r["fix"])
