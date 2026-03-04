# self-healing-agent

🤖 Self-Healing Agent
An autonomous multi-agent system that detects failing CI pipelines, diagnoses bugs, writes fixes, validates them locally, and opens a Pull Request — all without human intervention.
Built with LangGraph, Ollama (Llama 3.2), and the GitHub API.

🎬 How It Works
Failing GitHub Actions CI
          ↓
   [Watcher Agent]      →  Polls GitHub API for failed workflow runs
          ↓
   [Planner Agent]      →  Reads source + test files, diagnoses the bug using LLM
          ↓
   [Coder Agent]        →  Writes the fix (retries up to 3x if needed)
          ↓
   [Validator Agent]    →  Runs pytest locally to verify the fix works
          ↓
   [PR Agent]           →  Creates a branch, commits the fix, opens a Pull Request

If the validator fails, the system loops back to the Coder agent and retries — up to MAX_RETRIES times.

🏗️ Architecture
self-healing-agent/
├── agents/
│   ├── watcher.py       # Detects failed GitHub Actions runs
│   ├── planner.py       # LLM-powered bug diagnosis
│   ├── coder.py         # LLM-powered fix generation
│   ├── validator.py     # Runs pytest to verify the fix
│   └── pr_agent.py      # Opens a GitHub Pull Request
├── tools/
│   ├── github_tools.py  # GitHub API: read files, create branches, open PRs
│   └── code_tools.py    # Local: run pytest, apply file edits
├── graph.py             # LangGraph state machine orchestration
├── config.py            # Configuration and environment variables
└── main.py              # Entry point


State Graph
watcher → planner → coder → validator ──(pass)──→ pr_agent → END
                      ↑         │
                      └──(fail)─┘  (retries up to MAX_RETRIES)

🚀 Getting Started
Prerequisites
	∙	GitHub Codespaces (or any Linux environment)
	∙	Ollama installed
	∙	GitHub Personal Access Token (with repo and workflow scopes)
Setup

1. Clone the repo
git clone https://github.com/uchihamadara69404/self-healing-agent.git
cd self-healing-agent

2. Install dependencies
pip install -r requirements.txt

3. Pull the model
ollama pull llama3.2

4. Set environment variables
export GH_TOKEN="your_github_pat"

5. Update config
Edit config.py and set your REPO_OWNER and REPO_NAME.

6. Run the agent
ollama serve > /dev/null 2>&1 &
python3 main.py

📋 Requirements
langgraph
langchain
langchain-ollama
PyGithub
pytest
python-dotenv

💡 Key Design Decisions
Why LangGraph? LangGraph’s state machine model is ideal for agent loops with conditional retries. The graph makes the control flow explicit and debuggable.
Why Ollama? Running inference locally means zero API costs, no rate limits, and full privacy. The model never leaves your machine.
Why separate agents? Each agent has a single responsibility — this makes the system easier to debug, test, and extend. Want to swap the LLM? Change one file.

🔭 What’s Next
	∙	Trigger agent automatically via GitHub Actions webhook
	∙	Support multi-file bug fixes
	∙	Add support for more languages (JavaScript, Go)
	∙	Slack/Discord notification when a PR is opened
	∙	GraphRAG-powered codebase understanding for larger repos

🧠 Concepts Demonstrated
	∙	Multi-agent orchestration with LangGraph state graphs
	∙	Agentic retry loops with conditional edges
	∙	Tool use — file I/O, subprocess, GitHub API
	∙	Local LLM inference with Ollama
	∙	CI/CD integration via GitHub Actions and GitHub API
	∙	Autonomous code repair from failure detection to merged PR

👤 Author
Mohammed Kaif Ali (@uchihamadara69404)
