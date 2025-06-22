import uuid

from dotenv import load_dotenv
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google import genai
from question_answering_agent.agent import Question_Answering_Agent
import asyncio

load_dotenv('question_answering_agent/.env')

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
else:
    raise RuntimeError("GOOGLE_API_KEY not found in .env file")

#creating instance of agent to pass to the loader


initial_state = {
        "user_name": "Brandon Hancock",
        "user_preferences": """
            I like to play Pickleball, Disc Golf, and Tennis.
            My favorite food is Mexican.
            My favorite TV show is Game of Thrones.
            Loves it when people like and subscribe to his YouTube channel.
        """,
    }


# Create a new session service to store state


    
async def main():
    session_service_stateful = InMemorySessionService()


    # Create a NEW session
    APP_NAME = "Brandon Bot"
    USER_ID = "brandon_hancock"
    SESSION_ID = str(uuid.uuid4())
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    agent_instance = Question_Answering_Agent(initial_state["user_name"], initial_state["user_preferences"])

    runner =  Runner(
        agent=agent_instance,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text="What is Brandon's favorite TV show?")]
    )
    print("==== Running Agent ====")
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"Final Response: {event.content.parts[0].text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    # Log all messages in the session
    print("=== Session Messages ===")

    # Log final Session state
    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")



asyncio.run(main())
