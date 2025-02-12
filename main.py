import json
import os
from crewai import Crew
from Tasks import analyze_task, validate_task

def start_bug_fix(error_details):
    """
    Orchestrates the AI-driven bug-fixing workflow.
    1. Extracts error details from Sentry.
    2. CrewAI agents analyze, validate, and generate the best fix.
    3. Saves the AI-generated fix as `fix.patch` for GitHub Actions.
    4. GitHub Actions will create a fix branch, apply the patch, commit it, and create a PR.
    """

    print("🚀 Starting AI-driven bug-fixing process...")

    # Initialize CrewAI with the required agents and tasks
    crew = Crew(
        agents=[analyze_task.agent, validate_task.agent],
        tasks=[analyze_task, validate_task],
        verbose=True
    )

    # AI-powered analysis, validation, and final fix selection
    fixed_code = crew.kickoff()

    # Extract the file path where the error occurred
    file_path = error_details.get("culprit").split(":")[0]

    # Ensure we have a valid file path
    if not file_path or not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' does not exist. Cannot apply fix.")
        return

    # Save the AI-generated fix as a patch file for GitHub Actions
    patch_content = f"""--- {file_path}
+++ {file_path}
{fixed_code}
"""

    with open("fix.patch", "w") as f:
        f.write(patch_content)

    print(f"✅ AI-generated fix saved as `fix.patch`. GitHub Actions will process the fix.")
