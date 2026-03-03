from tools.github_tools import get_failed_workflow_runs, get_workflow_logs


def watcher_agent():
    """
    Watches GitHub Actions for failed runs.
    Returns the most recent failure with its logs.
    """
    print("🔍 Watcher: Checking for failed workflow runs...")

    failed_runs = get_failed_workflow_runs()

    if not failed_runs:
        print("✅ Watcher: No failed runs found.")
        return None

    # Take the most recent failure
    latest = failed_runs[0]
    print(f"❌ Watcher: Found failed run — {latest['name']} on branch '{latest['head_branch']}'")
    print(f"   URL: {latest['html_url']}")

    # Get logs for the failed run
    logs = get_workflow_logs(latest["id"])

    return {
        "run_id": latest["id"],
        "run_name": latest["name"],
        "branch": latest["head_branch"],
        "sha": latest["head_sha"],
        "url": latest["html_url"],
        "failed_steps": logs
    }
