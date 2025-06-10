import uuid
from google.adk.tools import FunctionTool
from app.schemas.ticket_state import TicketState, TicketCategory, TicketPriority

# The tool's return type hint MUST be TicketState.
# This is the official signal to the ADK framework that the return value of
# this function should be saved as the new session state.
def analyze_and_create_ticket(
    user_query: str, 
    category: TicketCategory, 
    priority: TicketPriority, 
    summary: str
) -> TicketState:
    """
    Analyzes user input to classify and summarize a support ticket. The returned
    TicketState object will be set as the new session state.
    
    Args:
        user_query: The original, unmodified query from the user.
        category: The classified category of the support ticket.
        priority: The assigned priority level of the ticket.
        summary: A concise, one-sentence summary of the user's issue.
    """
    print("✅ Tool 'analyze_and_create_ticket' called successfully.")
    
    new_ticket = TicketState(
        ticket_id=str(uuid.uuid4()),
        user_query=user_query,
        category=category,
        priority=priority,
        summary=summary,
        status="open"
    )
    
    print(f"   - Created and returning new ticket with ID: {new_ticket.ticket_id}")
    
    # --- THIS IS THE CRITICAL FIX ---
    # By returning the Pydantic object, we instruct the ADK to save it as
    # the new state for the session. This is the correct, simple pattern.
    return new_ticket
    # --------------------------------

analyze_and_create_ticket_tool = FunctionTool(analyze_and_create_ticket)