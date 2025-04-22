import os
import asyncio

from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types # For creating message Content/Parts
from google import genai


from dotenv import load_dotenv

from llms.gemini import runner_gemini
from llms.claude import runner_claude
from llms.gpt import runner_gpt

from tools.weather import get_weather
from memory import  USER_ID, SESSION_ID


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")

load_dotenv()

# --- IMPORTANT: Replace placeholders with your real API keys ---

# Gemini API Key (Get from Google AI Studio: https://aistudio.google.com/app/apikey)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") # <--- REPLACE

# OpenAI API Key (Get from OpenAI Platform: https://platform.openai.com/api-keys)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY') # <--- REPLACE

# Anthropic API Key (Get from Anthropic Console: https://console.anthropic.com/settings/keys)
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY') # <--- REPLACE


# --- Verify Keys (Optional Check) ---
print("API Keys Set:")
print(f"Google API Key set: {'Yes' if os.environ.get('GOOGLE_API_KEY') and os.environ['GOOGLE_API_KEY'] != 'GOOGLE_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
print(f"OpenAI API Key set: {'Yes' if os.environ.get('OPENAI_API_KEY') and os.environ['OPENAI_API_KEY'] != 'OPENAI_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")
print(f"Anthropic API Key set: {'Yes' if os.environ.get('ANTHROPIC_API_KEY') and os.environ['ANTHROPIC_API_KEY'] != 'ANTHROPIC_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")

# client = genai.client.Client(http_options=types.HttpOptions(api_version='v1'))
# client = genai.client.Client(http_options=types.HttpOptions(api_version='v1beta')) // default



# async def list_models():
#     r = await client.aio.models.list(config={'page_size': 5})
#     models = list(r.page)
#
#     for m in models:
#         print(f"\nModel Name: {m.name}")
#         print(f"Display Name: {m.display_name}")
#         print(f"Description: {m.description}")
#         print(f"Version: {m.version}")
#         print(f"Input Token Limit: {m.input_token_limit}")
#         print(f"Output Token Limit: {m.output_token_limit}")
#         print(f"Supported Actions: {m.supported_actions}")

    # [Model(name='projects/./locations/./models/123', display_name='my_model'



# Configure ADK to use API keys directly (not Vertex AI for this multi-model setup)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

runner = runner_gemini

# @title Define Agent Interaction Function
import asyncio
from google.genai import types # For creating message Content/Parts

async def call_agent_async(query: str):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])
  print('types.Part(text=query)===', types.Part(text=query))
  print('content===', content)

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")

  # @title Run the Initial Conversation

  # We need an async function to await our interaction helper
async def run_conversation():
    await call_agent_async("What is the weather like in London?")
    await call_agent_async("How about Paris?")
    await call_agent_async("Tell me the weather in New York")

if __name__ == "__main__":
  # asyncio.run(list_models())
  asyncio.run(run_conversation())
