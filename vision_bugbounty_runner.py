from modules.source_analyzer import SourceAnalyzer
from modules.llm_reasoner import LLMReasoner

code = open("target_source_code.txt").read()

analyzer = SourceAnalyzer()
reasoner = LLMReasoner()

findings = analyzer.analyze(code)
explanations = reasoner.analyze_findings(findings)

print("=== VISION BUG BOUNTY ANALYSIS ===")
for e in explanations:
    print(e)
