"""
Agent loader module - loads all agents from the agents folder and creates AgentOS.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Any, List

from agno.team import Team
from agno.agent import Agent
from agno.os import AgentOS


def load_all_agents_and_teams() -> List[Any]:
    """
    Dynamically load all agents from the agents folder.

    Each agent module should have
    - a `get_agents()` function that returns a list of Agent instances, and
    - a `get_teams()` function that returns a list of Team instances.

    Returns:
        List of all loaded Agent instances and Team instances
        in the order they were loaded.
    """
    agents: List[Agent] = []
    teams: List[Team] = []

    # Import agents package
    import agents as agents_pkg

    # Iterate through all modules in the agents package
    for importer, modname, ispkg in pkgutil.iter_modules(agents_pkg.__path__):
        if modname.startswith("_"):
            continue

        try:
            module = importlib.import_module(f"agents.{modname}")
        except Exception as e:
            print(f"✗ Failed to load agents.{modname}: {e}")
            continue

        # Check if module has get_agents function
        if hasattr(module, "get_agents"):
            module_agents = module.get_agents()
            agents.extend(module_agents)
            print(f"✓ Loaded {len(module_agents)} agents from agents.{modname}")
        else:
            print(f"⚠ Module agents.{modname} has no get_agents() function")

        # Check if module has get_teams function
        if hasattr(module, "get_teams"):
            module_teams = module.get_teams()
            teams.extend(module_teams)
            print(f"✓ Loaded {len(module_teams)} teams from agents.{modname}")
        else:
            print(f"⚠ Module agents.{modname} has no get_teams() function")

    return agents, teams


def create_agent_os(
    os_id: str = "finagent-os",
    description: str = "Financial Advisor Agent OS for Indians",
    agents: List[Agent] | None = None,
) -> AgentOS:
    """
    Create an AgentOS instance with all loaded agents.

    Args:
        os_id: Unique identifier for the AgentOS
        description: Description of the AgentOS
        agents: Optional list of agents. If None, loads all agents from agents folder.

    Returns:
        Configured AgentOS instance
    """
    if agents is None:
        agents, teams = load_all_agents_and_teams()

    if not agents and not teams:
        print(
            "⚠ No agents or teams loaded. AgentOS will be created with empty agent list."
        )
    else:
        print(f"✓ Creating AgentOS with {len(agents)} agents and {len(teams)} teams")

    return AgentOS(
        id=os_id,
        description=description,
        agents=agents,
        teams=teams,
    )


def run_agent_os(
    port: int = 5111,
    reload: bool = True,
    os_id: str = "finagent-os",
    description: str = "Financial Advisor Agent OS for Indians",
) -> None:
    """
    Create and run the AgentOS server.

    Args:
        port: Port to run the server on
        reload: Enable hot-reloading
        os_id: Unique identifier for the AgentOS
        description: Description of the AgentOS
    """
    agent_os = create_agent_os(os_id=os_id, description=description)
    app = agent_os.get_app()

    # The app reference needs to be in __main__ for reload to work
    agent_os.serve(app="main:app", reload=reload, port=port)
