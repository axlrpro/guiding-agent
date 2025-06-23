from google.adk.agents import SequentialAgent
from .steps_provider import steps_provider
from .code_generator import code_generator
from .code_runner import code_runner

root_agent = SequentialAgent(
    name="guiding_agent",
    description="A pipeline to take in user desired tasks, search its solution, generate the code to accomplish solution, and finally run the code.",
    sub_agents=[steps_provider, code_generator, code_runner]
)