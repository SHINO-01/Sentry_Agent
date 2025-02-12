# tasks.py
from crewai import Task
from Agents import bug_analyzer, bug_validator

# 🟢 Task 1: Bug Analysis & Proposed Fixes
analyze_task = Task(
    description="""
        Examine the Sentry error details and determine the root cause.
        Provide multiple possible fixes, explaining the pros and cons of each.
    """,
    expected_output="A list of possible fixes, including justifications.",
    agent=bug_analyzer,
    tools=bug_analyzer.tools
)

# 🔵 Task 2: Fix Validation & Selection
validate_task = Task(
    description="""
        Review all proposed fixes and select the most reliable one.
        Validate against best practices.
    """,
    expected_output="The most optimal fix after review and debate.",
    agent=bug_validator,
    tools=bug_validator.tools
)
