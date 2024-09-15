# utils/recommendations.py
from utils.chroma_manager import get_chroma_client
from langchain.embeddings.openai import OpenAIEmbeddings

def get_recommendations(query):
    embeddings = OpenAIEmbeddings()
    query_embedding = embeddings.embed_query(query)
    client = get_chroma_client()
    collection = client.get_or_create_collection('pdf_embeddings')
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=['metadatas']
    )
    recommended_pdfs = [metadata['pdf_name'] for metadata in results['metadatas'][0]]
    return set(recommended_pdfs)