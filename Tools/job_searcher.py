import os
from dotenv import load_dotenv
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from google.adk.tools.agent_tool import AgentTool

# Initialize client
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Init Chroma client (persistent storage)
client = chromadb.PersistentClient(path="../chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="jobs",
    metadata={"hnsw:space": "cosine"}  # use cosine similarity
)

def search_jobs_chroma(resume_text, top_k=5, filters=None):
    embedding = model.encode([resume_text])[0]

    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=top_k,
        where=filters  # e.g., {"job_location": "Berlin", "job_type": "Full-time"}
    )

    jobs = []
    for i in range(len(results["ids"][0])):
        jobs.append({
            "similarity_score": results["distances"][0][i],
            **results["metadatas"][0][i],
        })
    return pd.DataFrame(jobs)


job_search_tool = AgentTool(
    name="search_jobs_chroma",
    description="Searches the Chroma job DB for suitable jobs",
    func=search_jobs_chroma
)