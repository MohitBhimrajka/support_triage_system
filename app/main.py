import asyncio
import os
import vertexai
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from app.agents.router import create_router_agent
from app.schemas.ticket_state import TicketState
from vertexai.generative_models import Content, Part

async def run_test(agent: Agent):
    print("==========================================================")
    print("🚀 STARTING LOCAL AGENT TEST RUN...")
    print("==========================================================")

    session_service = InMemorySessionService()
    app_name = "support_triage_system"
    user_id = "test-user-123"

    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    session_id = session.id
    print(f"✅ Session created successfully with ID: {session_id}")

    runner = Runner(app_name=app_name, agent=agent, session_service=session_service)

    user_message_text = (
        "Hi, I can't seem to log into my account. I've tried resetting my"
        " password multiple times from the password reset page, but I never"
        " receive the email. I'm on a tight deadline and this is blocking me."
        " Can someone please help me urgently?"
    )
    print(f"💬 USER MESSAGE: '{user_message_text}'")
    
    user_message_content = Content(parts=[Part.from_text(user_message_text)])

    print("\n------------------ AGENT IS THINKING -------------------\n")
    
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message_content
    ):
        print(f"🔄 Agent event processed...")

    print("\n----------------- AGENT EXECUTION ENDED ----------------\n")
    
    final_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    final_state = final_session.state
    final_message = "I have analyzed your request and created a ticket. Someone will be in touch shortly."

    print(f"✅ FINAL AGENT RESPONSE (for user):\n{final_message}")
    
    print("\n🔍 FINAL SESSION STATE:")
    if isinstance(final_state, TicketState):
        print(final_state.model_dump_json(indent=2))
    elif final_state:
        print(f"⚠️  Unexpected state type: {type(final_state)}\n{final_state}")
    else:
        print("State was not updated or found.")

    print("\n==========================================================")
    print("🏁 TEST RUN COMPLETE")
    print("==========================================================")

if __name__ == "__main__":
    try:
        PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
        LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print(f"✅ Vertex AI SDK initialized for project {PROJECT_ID}.")
    except KeyError:
        print("🔴 ERROR: Make sure to set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables.")
        exit(1)

    my_router_agent = create_router_agent()
    asyncio.run(run_test(agent=my_router_agent))