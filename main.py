import os

from utils import call_agent_async
from dotenv import load_dotenv
import asyncio

from agents.root_gemini import root_gemini_agent
from agents.gemini import gemini_agent
from agents.claude import runner_claude
from agents.gpt import runner_gpt

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


async def run_conversation():
    await root_gemini_agent("hi")
    # await root_gemini_agent("What is the weather like in London?")
    # await gemini_agent("What is the weather like in London?")
    # await call_agent_async("How about Paris?", runner)
    # await call_agent_async("Tell me the weather in New York", runner)

if __name__ == "__main__":
  # asyncio.run(list_models())
  asyncio.run(run_conversation())
