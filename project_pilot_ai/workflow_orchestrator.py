class WorkflowOrchestrator:
    def __init__(self, extractor, analyzer, github_agent):
        self.extractor = extractor
        self.analyzer = analyzer
        self.github_agent = github_agent

    def run(self, transcript):
        tasks = self.extractor.extract_tasks(transcript)
        structure_report = self.analyzer.suggest_improvements()

        issue_links = []
        for task in tasks:
            issue_url = self.github_agent.create_issue(
                title=task["task"],
                assignee=task["owner"]
            )
            issue_links.append(issue_url)

        return {
            "tasks": tasks,
            "structure": structure_report,
            "issues_created": issue_links
        }
