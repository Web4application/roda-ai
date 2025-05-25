from fastapi import APIRouter, Request
from project_pilot_ai.workflow_orchestrator import WorkflowOrchestrator
from project_pilot_ai.task_extractor import TaskExtractor
from project_pilot_ai.repo_analyzer import RepoAnalyzer
from project_pilot_ai.github_agent import GitHubAgent

router = APIRouter()

@router.post("/projectpilot/analyze/")
async def projectpilot_analyze(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    base_path = data.get("base_path", ".")

    extractor = TaskExtractor()
    analyzer = RepoAnalyzer(base_path=base_path)
    github_agent = GitHubAgent()

    orchestrator = WorkflowOrchestrator(extractor, analyzer, github_agent)
    result = orchestrator.run(transcript)
    return result
