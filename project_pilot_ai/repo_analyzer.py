import os

class RepoAnalyzer:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def analyze_structure(self):
        required = ['README.md', 'tests/', 'src/', '.github/workflows/']
        missing = []
        for item in required:
            if not os.path.exists(os.path.join(self.base_path, item)):
                missing.append(item)
        return missing

    def suggest_improvements(self):
        return {
            "missing": self.analyze_structure(),
            "recommendations": [
                "Add CONTRIBUTING.md",
                "Setup automated CI/CD workflows",
                "Separate production and dev configs"
            ]
        }
