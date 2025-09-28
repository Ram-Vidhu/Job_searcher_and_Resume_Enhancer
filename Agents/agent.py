from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from .prompt import MAIN_AGENT_PROMPT
from .job_searcher.agent import job_searcher_agent
from .resume_parser.agent import resume_parser_agent

# Configure Gemini
MODEL = "gemini-2.5-flash"

# --- Agents ---
main_agent = LlmAgent(
    name="main",
    instruction=MAIN_AGENT_PROMPT,
    model=MODEL,
    sub_agents=[resume_parser_agent, job_searcher_agent]
)

root_agent = main_agent