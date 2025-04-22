# @title Define and Test GPT Agent
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools.weather import get_weather
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from main import call_agent_async
import asyncio


# Make sure 'get_weather' function from Step 1 is defined in your environment.
# Make sure 'call_agent_async' is defined from earlier.
MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-3-sonnet-20240229"
# --- Agent using GPT-4o ---
weather_agent_gpt = None # Initialize to None
runner_gemini = None      # Initialize runner to None

async def test_gpt_agent():
    try:
        MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"  # on the live api
        MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash-preview-04-17"
        MODEL_GEMINI_2_5_PRO = "gemini-2.5-pro-preview-03-25"

        AGENT_MODEL = MODEL_GEMINI_2_5_FLASH  # Starting with a powerful Gemini model

        weather_agent_gemini = Agent(
            name="weather_agent_v1",
            model=AGENT_MODEL,  # Specifies the underlying LLM
            description="Provides weather information for specific cities.",  # Crucial for delegation later
            instruction="You are a helpful weather assistant. Your primary goal is to provide current weather reports. "
                        "When the user asks for the weather in a specific city, "
                        "you MUST use the 'get_weather' tool to find the information. "
                        "Analyze the tool's response: if the status is 'error', inform the user politely about the error message. "
                        "If the status is 'success', present the weather 'report' clearly and concisely to the user. "
                        "Only use the tool when a city is mentioned for a weather request.",
            tools=[get_weather],  # Make the tool available to this agent
        )

        print(f"Agent '{weather_agent_gemini.name}' created using model '{AGENT_MODEL}'.")

        # InMemorySessionService is simple, non-persistent storage for this tutorial.
        session_service_gemini = InMemorySessionService()  # Create a dedicated service

        # Define constants for identifying the interaction context
        APP_NAME_GEMINI = "weather_tutorial_app_gemini"  # Unique app name for this test
        USER_ID_GEMINI = "user_1_gemini"
        SESSION_ID_GEMINI = "session_001_gemini"  # Using a fixed ID for simplicity

        # Create the specific session where the conversation will happen
        session_gemini = session_service_gemini.create_session(
            app_name=APP_NAME_GEMINI,
            user_id=USER_ID_GEMINI,
            session_id=SESSION_ID_GEMINI
        )
        print(f"Session created: App='{APP_NAME_GEMINI}', User='{USER_ID_GEMINI}', Session='{SESSION_ID_GEMINI}'")


        runner_gemini = Runner(
            agent=weather_agent_gemini,
            app_name=APP_NAME_GEMINI,
            session_service=session_service_gemini
        )
        print(f"Runner created for agent '{runner_gemini.agent.name}'.")

        print("\n--- Testing GEMINI Agent ---")
        # Ensure call_agent_async uses the correct runner, user_id, session_id
        await call_agent_async(query = "What's the weather in Tokyo?")

    except Exception as e:
        print(f"❌ Could not create or run GPT agent '{MODEL_GPT_4O}'. Check API Key and model name. Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gpt_agent())