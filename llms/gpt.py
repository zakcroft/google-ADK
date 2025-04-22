# @title Define and Test GPT Agent
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools.weather import get_weather
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from main import call_agent_async
import asyncio

MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-3-sonnet-20240229"

weather_agent_gpt = None
runner_gpt = None

async def test_gpt_agent():
    try:
        weather_agent_gpt = Agent(
            name="weather_agent_gpt",
            model=LiteLlm(model=MODEL_GPT_4O),
            description="Provides weather information (using GPT-4o).",
            instruction="You are a helpful weather assistant powered by GPT-4o. "
                        "Use the 'get_weather' tool for city weather requests. "
                        "Clearly present successful reports or polite error messages based on the tool's output status.",
            tools=[get_weather], # Re-use the same tool
        )
        print(f"Agent '{weather_agent_gpt.name}' created using model '{MODEL_GPT_4O}'.")

        # InMemorySessionService is simple, non-persistent storage for this tutorial.
        session_service_gpt = InMemorySessionService() # Create a dedicated service

        # Define constants for identifying the interaction context
        APP_NAME_GPT = "weather_tutorial_app_gpt" # Unique app name for this test
        USER_ID_GPT = "user_1_gpt"
        SESSION_ID_GPT = "session_001_gpt" # Using a fixed ID for simplicity

        # Create the specific session where the conversation will happen
        session_gpt = session_service_gpt.create_session(
            app_name=APP_NAME_GPT,
            user_id=USER_ID_GPT,
            session_id=SESSION_ID_GPT
        )
        print(f"Session created: App='{APP_NAME_GPT}', User='{USER_ID_GPT}', Session='{SESSION_ID_GPT}'")

        # Create a runner specific to this agent and its session service
        runner_gpt = Runner(
            agent=weather_agent_gpt,
            app_name=APP_NAME_GPT,       # Use the specific app name
            session_service=session_service_gpt # Use the specific session service
            )
        print(f"Runner created for agent '{runner_gpt.agent.name}'.")

        # --- Test the GPT Agent ---
        print("\n--- Testing GPT Agent ---")
        # Ensure call_agent_async uses the correct runner, user_id, session_id
        await call_agent_async(query = "What's the weather in Tokyo?",
                               runner=runner_gpt,
                               user_id=USER_ID_GPT,
                               session_id=SESSION_ID_GPT)

    except Exception as e:
        print(f"❌ Could not create or run GPT agent '{MODEL_GPT_4O}'. Check API Key and model name. Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gpt_agent())