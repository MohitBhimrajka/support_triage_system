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
    """
    Runs a single test case against the provided agent.
    """
    print("==========================================================")
    print("🚀 STARTING LOCAL AGENT TEST RUN...")
    print("==========================================================")

    session_service = InMemorySessionService()
    app_name = "support_triage_system"
    user_id = "test-user-123"

    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    print(f"✅ Session created successfully with ID: {session.id}")

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
    
    # --- This is the corrected, simpler loop ---
    # The runner yields events. We'll just capture the very last one,
    # which contains the final state of the conversation.
    final_event = None
    for event in runner.run(
        user_id=user_id,
        session_id=session.id,
        new_message=user_message_content
    ):
        print(f"🔄 Agent event processed...")
        final_event = event

    print("\n----------------- AGENT EXECUTION ENDED ----------------\n")
    
    if not final_event:
        print("❌ ERROR: The agent did not produce any output.")
        return

    # Extract the final message and state safely from the last event.
    final_message = getattr(final_event, 'message', "Agent did not produce a final message.")
    final_state = getattr(final_event.session, 'state', None)

    print(f"✅ FINAL AGENT RESPONSE (for user):\n{final_message}")
    
    print("\n🔍 FINAL SESSION STATE:")
    if isinstance(final_state, TicketState):
        print(final_state.model_dump_json(indent=2))
    elif final_state:
        print(f"⚠️  Unexpected state type: {type(final_state)}\n{final_state}")
    else:
        print("State was not updated.")

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