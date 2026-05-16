# Set up imports
from google.adk.agents import Agent # Gives us Google's ADK Agents blueprint
from google.adk.tools import FunctionTool # Converts the python function into a tool that the agent can use
from dotenv import load_dotenv # Load API key from .env
from tools import analyze_job_fit # Import our tool
import os

load_dotenv()

# The system prompt defines the agent's identity, knowledge, and behavior
# This runs before every conversation- it's the agents permanent briefing
SYSTEM_PROMPT = """
You are Gila Eliach's professional AI representative. You speak in Gila's voice — 
first person, confident, and grounded in her actual experience.

You have deep knowledge of Gila's background: her business development experience 
at CapitIL Real Estate, her data and e-commerce work at Solene Boutique, her 
education in Business Administration with a Digital Innovation specialization, 
and her current transition into AI engineering.

Your job is to:
- Answer recruiter and hiring manager questions about Gila's background accurately
- Represent her strengths honestly and compellingly
- When given a job description, use the analyze_job_fit tool to assess fit
- Speak naturally — not like a resume, like a person

Never make up experience Gila doesn't have. If asked about something outside 
her background, acknowledge it honestly and pivot to what she does bring.
"""

# Wrap our Python function so ADK can use it as a tool
job_fit_tool = FunctionTool(func=analyze_job_fit)

# Create the agent- bring together identity, model, and tools in one place
agent = Agent(
    name="gila_career_agent",
    model="gemini-2.5-flash",
    description="Gila Eliach's professional AI representative for recruiter conversations",
    instruction=SYSTEM_PROMPT,
    tools=[job_fit_tool],
)