from tools.github_tools import create_branch, commit_fix, open_pull_request


def pr_agent(failure_info: dict, coder_info: dict, plan_info: dict):
    """
    Creates a branch, commits the fix, and opens a PR.
    """
    print("🚀 PR Agent: Opening pull request...")

    branch_name = f"fix/auto-heal-{failure_info['run_id']}"

    # Create a new branch
    create_branch(branch_name)
    print(f"🌿 PR Agent: Created branch '{branch_name}'")

    # Commit the fix to the new branch
    commit_fix(
        filepath=coder_info["filepath"],
        new_content=coder_info["fixed_content"],
        branch_name=branch_name,
        commit_message=f"fix: auto-heal failing CI run #{failure_info['run_id']}"
    )
    print(f"📝 PR Agent: Committed fix to '{branch_name}'")

    # Open the PR
    pr_body = f"""## 🤖 Auto-generated fix by Self-Healing Agent

### Failed Workflow
- Run: [{failure_info['run_name']}]({failure_info['url']})
- Branch: `{failure_info['branch']}`

### Diagnosis
{plan_info['plan'][:500]}...

### Changes
Fixed `{coder_info['filepath']}`

> ✅ Fix verified locally by validator agent before opening this PR.
"""

    result = open_pull_request(
        branch_name=branch_name,
        title=f"🤖 Auto-fix: {failure_info['run_name']}",
        body=pr_body
    )

    print(f"✅ PR Agent: {result}")
    return result
