import os
from dotenv import load_dotenv
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

# Embedding model
sent_transform = SentenceTransformer("all-MiniLM-L6-v2")

# Init Chroma client (persistent storage)
client = chromadb.PersistentClient(path="../chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="jobs",
    metadata={"hnsw:space": "cosine"}  # use cosine similarity
)

def search_jobs_chroma(resume_text, top_k=5, filters=None):
    embedding = sent_transform.encode([resume_text])[0]

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
