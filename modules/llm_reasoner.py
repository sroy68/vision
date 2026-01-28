class LLMReasoner:
    def analyze_findings(self, findings: list):
        explanations = []

        for f in findings:
            explanations.append(
                f"Problem: {f['issue']}\n"
                f"Why dangerous: {f['impact']}\n"
                f"Recommended fix: {f['fix']}\n"
            )

        return explanations
