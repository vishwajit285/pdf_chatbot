# utils/summarization.py
from utils.chroma_manager import get_chroma_client
from langchain.llms import OpenAI

def summarize_documents():
    client = get_chroma_client()
    collection = client.get_or_create_collection('pdf_embeddings')
    documents = collection.get()['documents']
    full_text = " ".join(documents)
    llm = OpenAI()
    prompt = f"Summarize the following text:\n\n{full_text}\n\nSummary:"
    summary = llm(prompt)
    return summary
