# @title Interact with the Agent Team
import asyncio  # Ensure asyncio is imported

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from utils import call_agent_async

from agents.root_gemini import weather_agent_team as root_agent

async def run_team_conversation():
    print("\n--- Testing Agent Team Delegation ---")
    session_service = InMemorySessionService()
    APP_NAME = "weather_tutorial_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"
    session = session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    runner_agent_team = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent '{root_agent.name}'.")

    # --- Interactions using await (correct within async def) ---
    await call_agent_async(query="Hello there!",
                           runner=runner_agent_team,
                           user_id=USER_ID,
                           session_id=SESSION_ID)
    await call_agent_async(query="What is the weather in New York?",
                           runner=runner_agent_team,
                           user_id=USER_ID,
                           session_id=SESSION_ID)
    await call_agent_async(query="Thanks, bye!",
                           runner=runner_agent_team,
                           user_id=USER_ID,
                           session_id=SESSION_ID)

if __name__ == "__main__":  # Ensures this runs only when script is executed directly
    print("Executing using 'asyncio.run()' (for standard Python scripts)...")
    try:
        # This creates an event loop, runs your async function, and closes the loop.
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
