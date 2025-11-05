from google.adk.agents import LlmAgent
from teacher_agent.sub_agents.memory_agent.prompt import MEMORY_AGENT_INSTRUCTIONS
from tools.db_connector import create_db_schema


memory_agent = LlmAgent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="The memory agent who is responsible of creating an in-memory database schema. He is the one that executes the SQL queries for"
                "in-memory db schema creation",
    instruction=MEMORY_AGENT_INSTRUCTIONS,
    tools=[create_db_schema],
)