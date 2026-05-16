# Imports from Google ADK
from google.adk.runners import Runner # Executes agents and manages tool calls
from google.adk.sessions import InMemorySessionService # Manages conversation history so the agent remembers what was said
from google.genai.types import Content, Part # To have the ADK format the message so the agent can understand and use them
# Imports from our files
from agent import agent # This is our agent
# Imports from standard library
import asyncio # Allows us to run async code (can handle waiting for Gemini's responses without freezing)- its a built-in python tool

async def main():
    # Set up session manager- this is what remembers conversation history
    session_service = InMemorySessionService()

    # Create a session- a single conversation instance with unique ID's
    session = await session_service.create_session(
        app_name="gila_career_agent",
        user_id="recruiter",
        session_id="session_1"
    )

    # Create the runner- connects the agent to the session service
    runner = Runner(
        agent=agent,
        app_name="gila_career_agent",
        session_service=session_service
    )

    print("Gila's Career Agent is ready. Type 'quit' to exit.\n")

    # The conversation loop- keeps running until user types "quit"
    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            print("Ending session.")
            break

        # Wrap the user's message in ADK's required format
        message = Content(parts=[Part(text=user_input)])

        # Send the message to the agent and stream the response
        async for response in runner.run_async(
            user_id="recruiter",
            session_id="session_1",
            new_message=message
        ):
            if response.is_final_response():
                print(f"Agent: {response.content.parts[0].text}\n")

# Run the script only when executed directly- not when imported by another file

if __name__ == "__main__":
    asyncio.run(main())