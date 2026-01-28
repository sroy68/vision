def explain_decision(problem, fix):
    return f"""
আমি এই সিদ্ধান্ত নিয়েছি কারণ:
- Problem detected: {problem}
- Best known safe fix: {fix}
- Risk level: LOW (Python-level only)
Owner approval required before execution.
"""
