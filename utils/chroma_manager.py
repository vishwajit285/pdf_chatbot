# utils/chroma_manager.py
import os
import chromadb
from chromadb.config import Settings

# def get_chroma_client():
#     persist_directory = 'data/chroma'
#     if not os.path.exists(persist_directory):
#         os.makedirs(persist_directory)
#     client = chromadb.Client(Settings(
#         chroma_db_impl='duckdb+parquet',
#         persist_directory=persist_directory
#     ))

def get_chroma_client():
    persist_directory = 'data/chroma'
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        
    # # Updated client initialization
    # client = chromadb.Client(Settings(
    #     chroma_db_impl='duckdb+parquet',
    #     persist_directory=persist_directory
    # ))
    client = chromadb.PersistentClient(path=persist_directory)
    
    return client

    return client

def persist_db(client):
    client.persist()

def get_all_documents():
    client = get_chroma_client()
    collection = client.get_or_create_collection('pdf_embeddings')
    results = collection.get()
    return results
