from google.genai import types # For creating message Content/Parts
from session_test.session_state_test import session_service_stateful
from session_test.consts import APP_NAME

async def call_agent_async(query: str, runner, user_id:str, session_id:str):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])
  print('types.Part(text=query)===', types.Part(text=query))
  print('content===', content)
  print('session_id===', session_id)

  # Verify the initial state was set correctly
  retrieved_session = runner.session_service.get_session(app_name=APP_NAME,
                                                           user_id=user_id,
                                                           session_id=session_id)
  print("\n--- Initial Session State in utils call agent async ---")
  if retrieved_session:
      print(retrieved_session.state)
  else:
      print("Error: Could not retrieve session.")

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")