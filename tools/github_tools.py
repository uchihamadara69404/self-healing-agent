from github import Github
from config import GH_TOKEN, REPO_OWNER, REPO_NAME

# Initialize GitHub client
g = Github(GH_TOKEN)
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")


def get_failed_workflow_runs():
    """Fetch the latest failed GitHub Actions workflow runs."""
    runs = repo.get_workflow_runs(status="failure")
    failed = []
    for run in runs[:5]:  # Check last 5 failed runs
        failed.append({
            "id": run.id,
            "name": run.name,
            "head_branch": run.head_branch,
            "head_sha": run.head_sha,
            "html_url": run.html_url,
            "created_at": str(run.created_at),
        })
    return failed


def get_workflow_logs(run_id: int):
    """Get logs from a failed workflow run."""
    run = repo.get_workflow_run(run_id)
    jobs = run.jobs()
    logs = []
    for job in jobs:
        for step in job.steps:
            if step.conclusion == "failure":
                logs.append({
                    "job": job.name,
                    "step": step.name,
                    "conclusion": step.conclusion,
                })
    return logs


def get_file_content(filepath: str, branch: str = "main"):
    """Read a file from the repo."""
    try:
        contents = repo.get_contents(filepath, ref=branch)
        return contents.decoded_content.decode("utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"


def get_repo_structure(path: str = ""):
    """List files in the repo."""
    try:
        contents = repo.get_contents(path)
        return [item.path for item in contents]
    except Exception as e:
        return f"Error reading repo structure: {str(e)}"


def create_branch(branch_name: str):
    """Create a new branch from main."""
    source = repo.get_branch("main")
    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=source.commit.sha
    )
    return f"Branch '{branch_name}' created."


def commit_fix(filepath: str, new_content: str, branch_name: str, commit_message: str):
    """Commit a file fix to a branch."""
    contents = repo.get_contents(filepath, ref=branch_name)
    repo.update_file(
        path=filepath,
        message=commit_message,
        content=new_content,
        sha=contents.sha,
        branch=branch_name
    )
    return f"Fix committed to {branch_name}"


def open_pull_request(branch_name: str, title: str, body: str):
    """Open a PR from the fix branch into main."""
    pr = repo.create_pull(
        title=title,
        body=body,
        head=branch_name,
        base="main"
    )
    return f"PR opened: {pr.html_url}"
