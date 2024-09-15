# utils/pdf_handler.py
import os
import hashlib
from datetime import datetime
import pdfplumber
import pytesseract
from PIL import Image
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from tqdm import tqdm
from utils.chroma_manager import get_chroma_client
from utils.security import encrypt_pdf
import streamlit as st

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
            else:
                # Perform OCR
                pil_image = page.to_image(resolution=300).original
                ocr_text = pytesseract.image_to_string(pil_image)
                text += ocr_text
    return text

def compute_md5(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

def process_and_store_pdf(pdf_path, tags=None):
    pdf_hash = compute_md5(pdf_path)
    client = get_chroma_client()
    collection = client.get_or_create_collection('pdf_embeddings')

    # Check if PDF is already embedded
    existing = collection.get(where={'pdf_hash': pdf_hash})
    if existing['ids']:
        print(f"{os.path.basename(pdf_path)} is already embedded.")
        st.info(f"{os.path.basename(pdf_path)} is already embedded.")
        return

    # Encrypt PDF
    # encrypt_pdf(pdf_path)

    text = extract_text_from_pdf(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    docs = []
    pdf_name = os.path.basename(pdf_path)
    pdf_base_name, pdf_ext = os.path.splitext(pdf_name)

    # Version control
    version = 1
    existing_files = [f for f in os.listdir('data/pdfs') if f.startswith(pdf_base_name)]
    if existing_files:
        version = len(existing_files)

    # Update metadata
    upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tags = ",".join(tags)
    if tags is None:
        # Automatic tagging using LLM
        llm = OpenAI()
        prompt = f"Extract key topics from the following text:\n\n{text}\n\nTopics:"
        generated_tags = llm(prompt).split(',')
        tags = [tag.strip() for tag in generated_tags]
        tags = ",".join(tags)
    progress_bar = st.progress(0)
    total_chunks = len(texts)
    for idx, chunk in enumerate(tqdm(texts, desc="Embedding Text")):
        st.write(f"Processing chunk {idx}: {chunk[:50]}...") 
        embedding_vector = embeddings.embed_documents([chunk])
        st.write(f"Embedding vector for chunk {idx}: {embedding_vector}")
        print({
                'pdf_hash': pdf_hash,
                'pdf_name': pdf_base_name,
                'version': version,
                'upload_date': upload_date,
                'tags': tags
            })
        docs.append({
            'id': f"{pdf_hash}_{idx}_v{version}",
            'document': chunk,
            'metadata': {
                'pdf_hash': pdf_hash,
                'pdf_name': pdf_base_name,
                'version': version,
                'upload_date': upload_date,
                'tags': tags
            },
            'embedding': embedding_vector[0]  # Add the embedding to the document
        })
        progress_bar.progress((idx + 1) / total_chunks)

    collection.add(
        documents=[doc['document'] for doc in docs],
        metadatas=[doc['metadata'] for doc in docs],
        ids=[doc['id'] for doc in docs],
        embeddings=[doc['embedding'] for doc in docs],  # Make sure embeddings are being added
    )


    print(f"{os.path.basename(pdf_path)} has been embedded and stored.")
