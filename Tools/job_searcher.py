

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

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
            **results["metadatas"][0][i]
        })
        return pd.DataFrame(jobs)