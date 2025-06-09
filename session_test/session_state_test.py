import asyncio

# adk

# Import necessary session components
from google.adk.sessions import InMemorySessionService

from session_test.consts import *

# Create a NEW session service instance for this state demonstration
session_service_stateful = InMemorySessionService()
print("✅ New InMemorySessionService created for state demonstration.")

# Define a NEW session ID for this part of the tutorial
# APP_NAME = "session_state_APP_NAME"
# SESSION_ID_STATEFUL = "session_state_demo_001"
# USER_ID_STATEFUL = "user_state_demo"

# Define initial state data - user prefers Celsius initially
initial_state = {
    "user_preference_temperature_unit": "Celsius"
}

async def run_session_state():
    session_stateful = await session_service_stateful.create_session(
        app_name=APP_NAME,  # Use the consistent app name
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL,
        state=initial_state  # <<< Initialize state during creation
    )
    print(f"✅ Session '{SESSION_ID_STATEFUL}' created for user '{USER_ID_STATEFUL}'.")

    # Verify the initial state was set correctly
    retrieved_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                                   user_id=USER_ID_STATEFUL,
                                                                   session_id=SESSION_ID_STATEFUL)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")


if __name__ == "__main__":
  asyncio.run(run_session_state())
