"""
FinAgent - Financial Advisor Agent OS for Indians

Main entry point for running the AgentOS server.
"""

from dotenv import load_dotenv

load_dotenv()

from core import create_agent_os

# Create the AgentOS with all agents loaded from the agents folder
agent_os = create_agent_os(
    os_id="finagent-os",
    description="Financial Advisor Agent OS for Indians - Personal Finance & Investment Helper",
)

# Get the FastAPI app (needed for reload functionality)
app = agent_os.get_app()


if __name__ == "__main__":
    # Run the server
    agent_os.serve(
        app="main:app",
        reload=True,
        port=5111,
    )
