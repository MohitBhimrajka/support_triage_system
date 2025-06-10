from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# An enumeration for our ticket categories.
# Using literals enforces that only these specific string values are allowed.
TicketCategory = Literal[
    "technical_issue",
    "billing_inquiry",
    "account_access",
    "general_question",
    "unknown"
]

# An enumeration for our ticket priorities.
TicketPriority = Literal["low", "normal", "high", "urgent"]

class TicketState(BaseModel):
    """
    Represents the complete state and context of a single support ticket.
    This schema is the single source of truth for a ticket's journey.
    """
    ticket_id: Optional[str] = Field(
        default=None,
        description="The unique identifier for the support ticket."
    )
    
    user_query: str = Field(
        ...,
        description="The original, unmodified query from the user."
    )

    category: TicketCategory = Field(
        default="unknown",
        description="The classified category of the support ticket."
    )

    priority: TicketPriority = Field(
        default="normal",
        description="The assigned priority level of the ticket."
    )

    summary: Optional[str] = Field(
        default=None,
        description="A concise, one-sentence summary of the user's issue."
    )
    
    status: str = Field(
        default="new",
        description="The current status of the ticket (e.g., new, open, pending, resolved)."
    )

    assigned_agent: Optional[str] = Field(
        default=None,
        description="The name of the specialist agent this ticket is assigned to."
    )

    resolution_steps: List[str] = Field(
        default_factory=list,
        description="A log of actions and steps taken to resolve the ticket."
    )

    class Config:
        # This allows the model to be used seamlessly with various data sources.
        use_enum_values = True