import subprocess
import requests
import os

# Repository details
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = "https://github.com/SHINO-01/Sentry_FastAPI"
REPO_NAME = "SHINO-01/Sentry_FastAPI"
BRANCH_NAME = "fix-ai-bug"

def create_fix_branch():
    """
    Creates a new branch for the AI-generated fix.
    """
    try:
        print(f"🌿 Creating new branch: {BRANCH_NAME}")
        subprocess.run(["git", "checkout", "-b", BRANCH_NAME], check=True)
        print("✅ Branch created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create branch: {e}")
        return False
    return True

def commit_fix():
    """
    Commits the AI-generated fix and pushes it to GitHub.
    """
    try:
        print("📂 Staging modified files...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🤖 AI-generated bug fix"], check=True)
        subprocess.run(["git", "push", "origin", BRANCH_NAME], check=True)
        print("✅ Fix committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to commit/push changes: {e}")
        return False
    return True

def create_pull_request():
    """
    Creates a pull request to merge the AI fix into the main branch.
    """
    url = f"https://api.github.com/repos/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    pr_data = {
        "title": "[AI Bug Fix] Automated Patch Application",
        "body": "This pull request contains an AI-generated bug fix. Please review and merge if everything looks good.",
        "head": BRANCH_NAME,
        "base": "main"
    }

    response = requests.post(url, json=pr_data, headers=headers)
    
    if response.status_code == 201:
        print(f"✅ Pull request created: {response.json().get('html_url')}")
    else:
        print(f"❌ Failed to create pull request: {response.text}")

def process_ai_fix():
    """
    Full process: creates a branch, commits the fix, pushes, and creates a PR.
    """
    if create_fix_branch() and commit_fix():
        create_pull_request()

def apply_patch():
    """
    Applies the AI-generated patch (fix.patch) to the codebase.
    """
    patch_file = "fix.patch"

    # Check if patch file exists
    if not os.path.exists(patch_file):
        print("❌ No patch file found. Skipping code modification.")
        return False

    try:
        print("🔧 Applying AI-generated patch...")
        subprocess.run(["git", "apply", patch_file], check=True)
        print("✅ Patch applied successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to apply patch: {e}")
        return False