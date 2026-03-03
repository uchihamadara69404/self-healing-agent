from tools.code_tools import run_tests


def validator_agent(coder_info: dict, test_dir: str = "."):
    """
    Runs pytest to verify the fix actually works.
    Returns whether tests passed.
    """
    print("🧪 Validator: Running tests...")

    if not coder_info["success"]:
        print("❌ Validator: Coder failed to produce a fix, skipping tests.")
        return {"passed": False, "output": "Coder did not produce a fix."}

    results = run_tests(test_dir)

    if results["passed"]:
        print("✅ Validator: All tests passed!")
    else:
        print("❌ Validator: Tests still failing.")
        print(results["stdout"][-500:])  # Print last 500 chars of output

    return {
        "passed": results["passed"],
        "output": results["stdout"],
        "errors": results["stderr"]
    }

