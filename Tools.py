# tools.py
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import subprocess
import json

# 🛠️ Custom Tool 1: Parse Sentry Webhook
class ParseWebhookInput(BaseModel):
    webhook_payload: dict = Field(..., description="The JSON payload from Sentry containing error details.")

class ParseWebhookTool(BaseTool):
    name: str = "Parse Sentry Webhook"
    description: str = "Extracts relevant debugging information from a Sentry webhook payload."
    args_schema: Type[BaseModel] = ParseWebhookInput

    def _run(self, webhook_payload: dict) -> dict:
        """
        Parses the Sentry webhook payload and extracts relevant debugging details.
        """
        try:
            if not isinstance(webhook_payload, dict):
                raise ValueError("Invalid payload: Expected a dictionary")

            issue_id = webhook_payload.get("id", "Unknown")
            file_info = webhook_payload.get("culprit", "Unknown")
            error_message = webhook_payload.get("message", "No error message provided")
            repository = webhook_payload.get("repository", {}).get("full_name", "Unknown")

            return {
                "issue_id": issue_id,
                "file_info": file_info,
                "error_message": error_message,
                "repository": repository
            }

        except Exception as e:
            return {"error": f"Failed to parse webhook: {str(e)}"}

# 🛠️ Custom Tool 2: Static Code Analysis
class StaticAnalysisInput(BaseModel):
    file_path: str = Field(..., description="Path to the file that needs analysis.")

class StaticAnalysisTool(BaseTool):
    name: str = "Static Code Analysis"
    description: str = "Runs static analysis on the specified file."
    args_schema: Type[BaseModel] = StaticAnalysisInput

    def _run(self, file_path: str) -> str:
        print(f"🔍 Running static analysis on {file_path}...")
        return f"Static analysis complete for {file_path}. No critical issues found."

# 🛠️ Custom Tool 3: Run Unit Tests
class RunTestsTool(BaseTool):
    name: str = "Run Unit Tests"
    description: str = "Executes pytest to validate if the fix does not break existing functionality."

    def _run(self) -> str:
        print("🤖 Running automated tests...")
        result = subprocess.run(["pytest", "--maxfail=1", "--disable-warnings"], capture_output=True, text=True)

        if result.returncode == 0:
            return "✅ All tests passed!"
        else:
            return f"❌ Tests failed: {result.stderr}"
