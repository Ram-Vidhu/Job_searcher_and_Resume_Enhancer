import os
from dotenv import load_dotenv
from google import genai
from google.adk.agents import LlmAgent
from .prompt import MAIN_AGENT_PROMPT
from .job_searcher.agent import job_searcher_agent
from .resume_parser.agent import resume_parser_agent

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = "gemini-2.5-flash"

# --- Agents ---
main_agent = LlmAgent(
    name="main",
    instructions=MAIN_AGENT_PROMPT,
    model=model,
    sub_agents=[resume_parser_agent, job_searcher_agent]
)

root_agent = main_agent