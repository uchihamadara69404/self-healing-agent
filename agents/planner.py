from tools.github_tools import get_file_content, get_repo_structure
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.2")




def planner_agent(failure_info: dict):
    """
    Reads the failed test + source files and diagnoses the bug.
    Returns a plan for fixing it.
    """
    print("🧠 Planner: Diagnosing the failure...")

    # Get repo structure to find relevant files
    structure = get_repo_structure()
    
    # Find test files and source files
    test_files = [f for f in structure if "test" in f.lower() and f.endswith(".py")]
    source_files = [f for f in structure if "test" not in f.lower() and f.endswith(".py")]

    # Read contents of relevant files
    file_contents = {}
    for filepath in test_files + source_files:
        file_contents[filepath] = get_file_content(filepath)

    # Build prompt for the planner
    files_text = "\n\n".join([
        f"### {path}\n```python\n{content}\n```"
        for path, content in file_contents.items()
    ])

    failed_steps_text = "\n".join([
        f"- Job: {s.get('job')}, Step: {s.get('step')}, Result: {s.get('conclusion')}"
        for s in failure_info.get("failed_steps", [])
    ])

    prompt = f"""You are an expert software engineer debugging a failing CI pipeline.

## Failed Workflow
- Run name: {failure_info['run_name']}
- Branch: {failure_info['branch']}
- Failed steps:
{failed_steps_text}

## Repository Files
{files_text}

## Your Task
1. Identify which file contains the bug
2. Explain what the bug is
3. Describe exactly how to fix it

Be specific. Reference exact function names and line numbers where possible.
IMPORTANT: The test file is correct and should NEVER be modified. Only the source file contains the bug.
"""

    response = llm.invoke(prompt)
    plan = response.content
    print(f"📋 Planner: Diagnosis complete.\n{plan[:300]}...")

    return {
        "plan": plan,
        "file_contents": file_contents,
        "test_files": test_files,
        "source_files": source_files
    }
