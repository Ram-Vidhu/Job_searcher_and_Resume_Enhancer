from google.adk.agents import LlmAgent
from .prompt import JOB_SEARCHER_PROMPT
from Tools.job_searcher import search_jobs_chroma

model = "gemini-2.5-flash"

job_searcher_agent = LlmAgent(
    name="job_searcher",
    instruction=JOB_SEARCHER_PROMPT,
    model=model,
    tools=[search_jobs_chroma]
)