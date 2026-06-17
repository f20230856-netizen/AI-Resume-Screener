import json
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from transformers import pipeline

def create_vectorstore(documents):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local("langchain_resume_index")
    return vectorstore

def decompose_job_description(query):
    flan_pipe = pipeline("text2text-generation", model="google/flan-t5-base")
    prompt = f"""
    Extract the following from this job description:
    - Key Skills
    - Required Experience
    - Education or Certifications

    Job Description:
    {query}
    """
    return flan_pipe(prompt, max_length=200, do_sample=False)[0]['generated_text']

def match_resumes(vectorstore, query, top_k=5):
    results = sorted(
        vectorstore.similarity_search_with_score(query, k=top_k),
        key=lambda x: x[1],
        reverse=True
    )
    matched_results = []
    for i, (doc, score) in enumerate(results, 1):
        similarity_percent = round(float(np.float64(min(score * 100, 100))), 2)
        preview = doc.page_content[:600]
        matched_results.append({
            "rank": i,
            "match_score_percent": similarity_percent,
            "raw_score": float(score),
            "resume_preview": preview
        })
    with open("matched_resumes.json", "w", encoding="utf-8") as f:
        json.dump(matched_results, f, indent=4)
    return matched_results