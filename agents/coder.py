from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_NAME
from tools.code_tools import apply_fix_locally

llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)


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

Only fix the file that contains the bug. Do not modify test files.
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
