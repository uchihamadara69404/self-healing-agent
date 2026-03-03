from graph import build_graph

def main():
    print("🤖 Self-Healing Agent Starting...\n")

    graph = build_graph()

    initial_state = {
        "failure_info": None,
        "plan_info": None,
        "coder_info": None,
        "validation_result": None,
        "pr_result": None,
        "retries": 0
    }

    result = graph.invoke(initial_state)

    print("\n--- Final State ---")
    if result.get("pr_result"):
        print(f"✅ Success! {result['pr_result']}")
    elif result.get("validation_result") and not result["validation_result"]["passed"]:
        print("❌ Agent could not fix the issue after max retries.")
    else:
        print("✅ No failures detected in the repo.")

if __name__ == "__main__":
    main()
