import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GH_TOKEN = os.environ.get("GH_TOKEN")

# Model config
MODEL_NAME = "llama-3.3-70b-versatile"  # Free on Groq, excellent at code

# GitHub config - update these to match your repo
REPO_OWNER = "uchihamadara69404"
REPO_NAME = "self-healing-agent"
TARGET_BRANCH = "main"

# Agent config
MAX_RETRIES = 3  # How many times coder agent retries before giving up
