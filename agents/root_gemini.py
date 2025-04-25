from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm

from agents.subs import greeting_agent, farewell_agent

from tools.weather import get_weather
from utils import call_agent_async

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"  # on the live api
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash-preview-04-17"
MODEL_GEMINI_2_5_PRO = "gemini-2.5-pro-preview-03-25"

AGENT_MODEL = MODEL_GEMINI_2_5_FLASH

weather_agent_team = None
runner_gemini = None

async def root_gemini_agent(query: str):
    if greeting_agent and farewell_agent and 'get_weather' in globals():
        try:

            weather_agent_team = Agent(
                name="weather_agent_v1",
                model=AGENT_MODEL,
                description="Provides weather information for specific cities.",  # Crucial for delegation later
                instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                            "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                            "You have specialized sub-agents: "
                            "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                            "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                            "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                            "If it's a weather request, handle it yourself using 'get_weather'. "
                            "For anything else, respond appropriately or state you cannot handle it.",
                tools=[get_weather],  # Make the tool available to this agent
                sub_agents=[greeting_agent, farewell_agent]
            )

            print(f"Agent '{weather_agent_team.name}' created using model '{AGENT_MODEL}'.")

            # InMemorySessionService is simple, non-persistent storage for this tutorial.
            session_service_gemini = InMemorySessionService()  # Create a dedicated service

            # Define constants for identifying the interaction context
            APP_NAME_GEMINI = "weather_app_gemini"  # Unique app name for this test
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
                agent=weather_agent_team,
                app_name=APP_NAME_GEMINI,
                session_service=session_service_gemini
            )

            print(f"Runner created for agent '{runner_gemini.agent.name}'.")

            # Ensure call_agent_async uses the correct runner, user_id, session_id
            await call_agent_async(query, runner_gemini, USER_ID_GEMINI, SESSION_ID_GEMINI)

        except Exception as e:
            print(f"❌ Could not create or run GEMINI agent '{AGENT_MODEL}'. Check API Key and model name. Error: {e}")
    else:
        print(
            "❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
        if not greeting_agent: print(" - Greeting Agent is missing.")
        if not farewell_agent: print(" - Farewell Agent is missing.")
        if 'get_weather' not in globals(): print(" - get_weather function is missing.")
# if __name__ == "__main__":
#     asyncio.run(gemini_agent())
