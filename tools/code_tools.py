import subprocess
import os
import tempfile


def run_tests(test_dir: str = "."):
    """Run pytest and return results."""
    result = subprocess.run(
        ["python3", "-m", "pytest", test_dir, "--tb=short", "-v"],
        capture_output=True,
        text=True,
        cwd=test_dir
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "passed": result.returncode == 0
    }


def apply_fix_locally(filepath: str, new_content: str):
    """Write fixed content to a local file."""
    try:
        with open(filepath, "w") as f:
            f.write(new_content)
        return f"Fix applied to {filepath}"
    except Exception as e:
        return f"Error applying fix: {str(e)}"


def read_local_file(filepath: str):
    """Read a local file."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def list_local_files(directory: str = "."):
    """List all Python files in a directory."""
    py_files = []
    for root, dirs, files in os.walk(directory):
        # Skip hidden dirs and common noise
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

