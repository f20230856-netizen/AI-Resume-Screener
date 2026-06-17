from document_loader import load_documents
from embed_and_query import create_vectorstore, decompose_job_description, match_resumes

if __name__ == "__main__":
    resume_folder = "sample_resumes"
    documents = load_documents(resume_folder)
    print(f"\nLoaded {len(documents)} document chunks.")

    vectorstore = create_vectorstore(documents)
    print("FAISS embedding index saved.\n")

    query = input("Enter a job description:\n> ")
    decomposed = decompose_job_description(query)
    print("\nDecomposed Job Description:\n", decomposed)

    match_resumes(vectorstore, query)
    print("\nMatching results written to matched_resumes.json")
