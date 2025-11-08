from google.adk.agents import LlmAgent
from teacher_agent.prompt import ROOT_INSTRUCTIONS
from teacher_agent.sub_agents.schema_designer_agent.agent import schema_designer_agent
from teacher_agent.sub_agents.quiz_agent.agent import quiz_agent
from teacher_agent.sub_agents.memory_agent.agent import memory_agent

root_agent = LlmAgent(
    name="teacher_agent",
    model="gemini-2.0-flash",
    description="The root agent called teacher_agent who delegates tasks related to SQL to sub-agents",
    instruction=ROOT_INSTRUCTIONS,
    sub_agents=[schema_designer_agent, memory_agent, quiz_agent],
)