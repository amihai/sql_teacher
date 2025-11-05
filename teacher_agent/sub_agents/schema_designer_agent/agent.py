from google.adk.agents import LlmAgent
from teacher_agent.sub_agents.schema_designer_agent.prompt import SCHEMA_DESIGNER_INSTRUCTIONS

schema_designer_agent = LlmAgent(
    name="schema_designer_agent",
    model="gemini-2.0-flash",
    description="The schema designer agent who is responsible of generating SQL schema based on user description",
    instruction=SCHEMA_DESIGNER_INSTRUCTIONS,
    output_key="designer_response",
)