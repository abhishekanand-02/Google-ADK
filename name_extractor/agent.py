"""
Name Extractor - Demonstrates Session State Basics

Shows how to use output_key to save data and access it via session.state.

Reference: https://google.github.io/adk-docs/sessions/state.md
"""

from google.adk.agents import LlmAgent

# Single agent that extracts and saves name: final reply is written to state["user_name"]
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="name_extractor",
    instruction="""
You extract the user's preferred name from what they say.

Rules:
- If they introduce themselves (e.g. "I'm Alex", "call me Sam"), reply with only that name.
- If no clear name is present, reply with exactly: UNKNOWN
- Reply with plain text only: no quotes, no extra sentences, no punctuation around the name.
""",
    output_key="user_name",
)
