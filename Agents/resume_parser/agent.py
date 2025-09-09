# agent.py

import os
import argparse
import json
from dotenv import load_dotenv
import google.generativeai as genai
from prompt import build_prompt
from PyPDF2 import PdfReader
import docx

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")  # Updated to 2.5 Flash

def read_resume_file(path: str) -> str:
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

def parse_resume(resume_text: str) -> dict:
    prompt = build_prompt(resume_text)
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Remove markdown fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")  # removes ```json and ```
        # Sometimes model puts "json\n{...}\n", so split at first '{'
        raw_text = raw_text[raw_text.find("{") : raw_text.rfind("}") + 1]

    try:
        return json.loads(raw_text)
    except Exception as e:
        return {"error": f"Failed to parse JSON: {e}", "raw": response.text}



parser = argparse.ArgumentParser(description="AI Resume Parser using Gemini 2.5 Flash")
parser.add_argument("resume_path", type=str, help="Path to resume file (txt/pdf/docx)")
args = parser.parse_args()

if not os.path.exists(args.resume_path):
    print(f"File not found: {args.resume_path}")
    exit(1)

try:
    resume = read_resume_file(args.resume_path)
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

result = parse_resume(resume)
print(json.dumps(result, indent=2))
