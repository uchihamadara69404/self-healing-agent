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

    prompt = f"""You are a Python bug fixer. Fix the bug in the source file.

## Diagnosis
{plan_info['plan']}

## Files
{files_text}

## STRICT OUTPUT FORMAT - follow exactly:
FILEPATH: calculator.py
CONTENT:
<only valid python code here, nothing else>

RULES:
- Output ONLY the two lines above then pure Python code
- NO backticks, NO markdown, NO explanations, NO comments about the fix
- NEVER output test files (files with 'test' in the name)
- ONLY output calculator.py
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

        # Parse the response
    try:
        lines = raw.split("\n")

        # Handle Format 1: FILEPATH/CONTENT structure
        if lines[0].startswith("FILEPATH:"):
            filepath = lines[0].replace("FILEPATH:", "").strip()
            content_start = next(i for i, l in enumerate(lines) if l.strip() == "CONTENT:") + 1
            fixed_content = "\n".join(lines[content_start:])

        # Handle Format 2: markdown code block anywhere in response
        elif "```python" in raw:
            code_start = raw.index("```python") + len("```python")
            code_end = raw.index("```", code_start)
            fixed_content = raw[code_start:code_end].strip()
            filepath = "calculator.py"

        # Handle Format 3: raw code dump
        else:
            filepath = "calculator.py"
            fixed_content = raw

        # Strip any remaining markdown fences
        fixed_content = fixed_content.strip()
        if fixed_content.startswith("```"):
            fixed_content = "\n".join(fixed_content.split("\n")[1:])
        if fixed_content.endswith("```"):
            fixed_content = "\n".join(fixed_content.split("\n")[:-1])

        # Safety check - never write to test files
        if "test" in filepath.lower():
            print("⚠️  Coder tried to modify a test file — rejecting!")
            return {"filepath": None, "fixed_content": None, "success": False}

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
