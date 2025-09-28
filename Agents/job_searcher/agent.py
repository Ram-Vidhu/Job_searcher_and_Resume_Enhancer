import os
from dotenv import load_dotenv
from google import genai
from google.adk import Agent
from .prompt import JOB_SEARCHER_PROMPT
from Tools.job_searcher import job_search_tool

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = "gemini-2.5-flash"

job_searcher_agent = Agent(
    name="job_searcher",
    instructions=JOB_SEARCHER_PROMPT,
    model=model,
    tools=[job_search_tool]
)