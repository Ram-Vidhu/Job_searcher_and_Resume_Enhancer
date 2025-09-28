# agent.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk import Agent
# from google.genai.agents import Agent, Tool
# from google.adk.tools.agent_tool import AgentTool
from PyPDF2 import PdfReader
import docx
from .prompt import RESUME_PARSER_PROMPT

# Setup
load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = "gemini-2.5-flash"

# Utilities (not tools, just helpers)
def read_resume_file(path: str) -> str:
    """Read resume text from txt/pdf/docx file."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        doc = docx.Document(path)
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# def build_prompt(resume_text: str) -> str:
#     """Build parser prompt with resume text."""
#     return f"{RESUME_PARSER_PROMPT}\n\nResume:\n{resume_text}\n"

# Core Tool
def parse_resume(resume_text: str) -> dict:
    """Extract structured info from resume text."""
    # prompt = build_prompt(resume_text)
    # response = model.generate_content(prompt)
    raw_text = resume_text

    # Clean markdown fences if model includes ```json ... ```
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text[raw_text.find("{") : raw_text.rfind("}") + 1]

    try:
        return json.loads(raw_text)
    except Exception as e:
        return {"error": f"Failed to parse JSON: {e}", "raw": resume_text}

# # Tool + Agent
# resume_parser_tool = AgentTool(
#     name="parse_resume",
#     description="Extracts role, skills, experience, last company, last location from a resume.",
#     func=parse_resume,
# )

resume_parser_agent = Agent(
    name="resume_parser",
    instruction=RESUME_PARSER_PROMPT,
    model=model,
    tools=[parse_resume, read_resume_file],
)
