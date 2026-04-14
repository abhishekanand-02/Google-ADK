"""
Test script to see session state access directly (Runner, no adk web).

From repo root (with venv activated):

    python name_extractor/test_state.py

Requires GOOGLE_API_KEY (or your usual ADK/Gemini env) for the model call.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

# Ensure `import agent` resolves when run as `python name_extractor/test_state.py`
_AGENT_DIR = Path(__file__).resolve().parent
if str(_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(_AGENT_DIR))

load_dotenv(_AGENT_DIR / ".env")

from agent import root_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP_NAME = "name_extractor"
USER_ID = "demo_user"
SESSION_ID = "demo_session"


async def main() -> None:
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = Content(
        role="user",
        parts=[Part(text="Hello, my name is Jamie.")],
    )

    async for _event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        pass

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    if not session:
        print("Session not found after run.")
        return

    print("Full session.state:", dict(session.state))
    print("user_name (from output_key):", session.state.get("user_name"))


if __name__ == "__main__":
    asyncio.run(main())
