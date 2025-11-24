from google.adk.agents import LlmAgent
from backend.teacher_agent.sub_agents.memory_agent.prompt import MEMORY_AGENT_INSTRUCTIONS
from backend.tools.db_connector import db_interactions


memory_agent = LlmAgent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="Responsible for managing and executing all SQL operations within an in-memory SQLite database",
    instruction=MEMORY_AGENT_INSTRUCTIONS,
    tools=[db_interactions],
)