import asyncio

from agents import runner_root_stateful
from consts import *
from session_test.session_state_test import session_service_stateful, run_session_state
from session_test.utils import call_agent_async


async def run_stateful_conversation():
    print(
        f"APP_NAME={APP_NAME}, USER_ID_STATEFUL={USER_ID}, SESSION_ID_STATEFUL={SESSION_ID}")

    await run_session_state()

    # Verify the initial state was set correctly
    retrieved_session = session_service_stateful.get_session(app_name=APP_NAME,
                                                             user_id=USER_ID,
                                                             session_id=SESSION_ID)
    print("\n--- Initial Session State after creation ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")


    # 1. Check weather (Uses initial state: Celsius)
    print("--- Turn 1: Requesting weather in London (expect Celsius) ---")

    await call_agent_async(query= "What's the weather in London?",
                           runner=runner_root_stateful,
                           user_id=USER_ID,
                           session_id=SESSION_ID
                          )

    # 2. Manually update state preference to Fahrenheit - DIRECTLY MODIFY STORAGE
    print("\n--- Manually Updating State: Setting unit to Fahrenheit ---")
    try:
        # Access the internal storage directly - THIS IS SPECIFIC TO InMemorySessionService for testing
        # NOTE: In production with persistent services (Database, VertexAI), you would
        # typically update state via agent actions or specific service APIs if available,
        # not by direct manipulation of internal storage.
        stored_session = session_service_stateful.sessions[APP_NAME][USER_ID][SESSION_ID]
        stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
        # Optional: You might want to update the timestamp as well if any logic depends on it
        # import time
        # stored_session.last_update_time = time.time()
        print(f"--- Stored session state updated. Current 'user_preference_temperature_unit': {stored_session.state.get('user_preference_temperature_unit', 'Not Set')} ---") # Added .get for safety
    except KeyError:
        print(f"--- Error: Could not retrieve session '{SESSION_ID}' from internal storage for user '{USER_ID}' in app '{APP_NAME}' to update state. Check IDs and if session was created. ---")
    except Exception as e:
         print(f"--- Error updating internal session state: {e} ---")

    # 3. Check weather again (Tool should now use Fahrenheit)
    # This will also update 'last_weather_report' via output_key
    print("\n--- Turn 2: Requesting weather in New York (expect Fahrenheit) ---")
    await call_agent_async(query= "Tell me the weather in New York.",
                           runner=runner_root_stateful,
                           user_id=USER_ID,
                           session_id=SESSION_ID
                          )

    # 4. Test basic delegation (should still work)
    # This will update 'last_weather_report' again, overwriting the NY weather report
    print("\n--- Turn 3: Sending a greeting ---")
    await call_agent_async(query= "Hi!",
                           runner=runner_root_stateful,
                           user_id=USER_ID,
                           session_id=SESSION_ID
                          )

# --- Execute the `run_stateful_conversation` async function ---
# Choose ONE of the methods below based on your environment.

# METHOD 1: Direct await (Default for Notebooks/Async REPLs)
# If your environment supports top-level await (like Colab/Jupyter notebooks),
# it means an event loop is already running, so you can directly await the function.
print("Attempting execution using 'await' (default for notebooks)...")
# await run_stateful_conversation()

# METHOD 2: asyncio.run (For Standard Python Scripts [.py])
# If running this code as a standard Python script from your terminal,
# the script context is synchronous. `asyncio.run()` is needed to
# create and manage an event loop to execute your async function.
# To use this method:
# 1. Comment out the `await run_stateful_conversation()` line above.
# 2. Uncomment the following block:

import asyncio
if __name__ == "__main__": # Ensures this runs only when script is executed directly
    print("Executing using 'asyncio.run()' (for standard Python scripts)...")
    try:
        # This creates an event loop, runs your async function, and closes the loop.
        asyncio.run(run_stateful_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Inspect final session state after the conversation ---
# This block runs after either execution method completes.
print("\n--- Inspecting Final Session State ---")
final_session = session_service_stateful.get_session(app_name=APP_NAME,
                                                     user_id= USER_ID,
                                                     session_id=SESSION_ID)
if final_session:
    # Use .get() for safer access to potentially missing keys
    print(f"Final Preference: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}")
    print(f"Final Last Weather Report (from output_key): {final_session.state.get('last_weather_report', 'Not Set')}")
    print(f"Final Last City Checked (by tool): {final_session.state.get('last_city_checked_stateful', 'Not Set')}")
    # Print full state for detailed view
    # print(f"Full State Dict: {final_session.state.as_dict()}") # Use as_dict() for clarity
else:
    print("\n❌ Error: Could not retrieve final session state.")

