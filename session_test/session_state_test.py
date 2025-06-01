import asyncio

# adk
from google.adk.sessions import InMemorySessionService
from consts import *

session_service_stateful = InMemorySessionService()
print("✅ New InMemorySessionService created.")

initial_state = {
    "user_preference_temperature_unit": "Celsius"
}

async def run_session_state():
    session_stateful = session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )
    print(f"✅ Session '{SESSION_ID}' created for user '{USER_ID}'.")

    # Verify the initial state was set correctly
    retrieved_session = session_service_stateful.get_session(app_name=APP_NAME,
                                                             user_id=USER_ID,
                                                             session_id=SESSION_ID)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")



if __name__ == "__main__":
  asyncio.run(run_session_state())
