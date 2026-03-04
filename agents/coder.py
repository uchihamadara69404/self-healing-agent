from langchain_ollama import ChatOllama

from tools.code_tools import apply_fix_locally

llm = ChatOllama(model="llama3.2")


def coder_agent(plan_info: dict):
    """
    Takes the planner's diagnosis and writes the actual fix.
    Returns the fixed file path and content.
    """
    print("💻 Coder: Writing the fix...")

    files_text = "\n\n".join([
        f"### {path}\n```python\n{content}\n```"
        for path, content in plan_info["file_contents"].items()
    ])

    prompt = f"""You are an expert software engineer. Your job is to fix a bug.

## Diagnosis & Plan
{plan_info['plan']}

## Current File Contents
{files_text}

## Your Task
Return ONLY the fixed Python file content — no explanation, no markdown, no backticks.
Your response must be in this exact format:

FILEPATH: <path/to/file.py>
CONTENT:
<full fixed file content here>

CRITICAL RULES:
- NEVER modify any file with 'test' in the name
- ONLY fix the source file (e.g. buggy_code.py)
- The test file is always correct — the source code must match what the tests expect
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Parse the response
    try:
        lines = raw.split("\n")
        filepath = lines[0].replace("FILEPATH:", "").strip()
        content_start = next(i for i, l in enumerate(lines) if l.strip() == "CONTENT:") + 1
        fixed_content = "\n".join(lines[content_start:])

        # Apply fix locally so validator can test it
        apply_fix_locally(filepath, fixed_content)
        print(f"🔧 Coder: Fix applied to {filepath}")

        return {
            "filepath": filepath,
            "fixed_content": fixed_content,
            "success": True
        }
    except Exception as e:
        print(f"❌ Coder: Failed to parse fix — {str(e)}")
        return {
            "filepath": None,
            "fixed_content": None,
            "success": False
        }
