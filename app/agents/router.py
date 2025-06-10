from google.adk.agents import Agent
# --- Import the new tool ---
from app.tools.triage_tools import create_structured_ticket_tool
from app.configs.loader import load_agent_configs

def create_router_agent() -> Agent:
    """
    Factory function to create and return a configured RouterAgent.
    """
    print("Creating RouterAgent instance...")
    all_configs = load_agent_configs()
    router_config = all_configs["RouterAgent"]

    router_agent = Agent(
        name="RouterAgent",
        model=router_config["model_name"],
        instruction=router_config["instruction"],
        # --- Use the new, simpler tool ---
        tools=[create_structured_ticket_tool],
    )
    
    print("✅ RouterAgent instance created successfully.")
    return router_agent