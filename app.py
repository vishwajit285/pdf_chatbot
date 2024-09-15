# app.py5
import streamlit as st
import os
import base64
import re
import json
from datetime import datetime
from utils.pdf_handler import process_and_store_pdf,display_pdf
from utils.retrieval import get_answer_conversational
from utils.summarization import summarize_documents
from utils.annotations import load_annotations, save_annotation
from utils.recommendations import get_recommendations
from utils.chroma_manager import get_chroma_client
from utils.security import encrypt_pdf, decrypt_pdf, load_key
from utils.visualization import generate_word_cloud
from utils.external_data import fetch_external_data
from utils.answer_audio_handler import generate_audio
from PIL import Image
from fpdf import FPDF
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import speech_recognition as sr
from gtts import gTTS
from utils.speech_handler import capture_voice_input
import tempfile



# Set custom page config
st.set_page_config(page_title="Multi-PDF Chatbot", page_icon="📚", layout="wide")
if 'voice_query' not in st.session_state:
    st.session_state.voice_query = ""
if 'text_query' not in st.session_state:
    st.session_state.text_query = ""
if 'generated_audio_file' not in st.session_state:
    st.session_state.generated_audio_file = None

# Custom CSS to style the app
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .st-button>button {
        background-color: #2c3e50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Main title
st.markdown("<h1>📚 Multi-PDF Chatbot</h1>", unsafe_allow_html=True)

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for PDF Upload
st.sidebar.header("📁 Upload PDFs")
uploaded_pdfs = st.sidebar.file_uploader("Choose PDFs", type=['pdf'], accept_multiple_files=True)

# Input for custom tags
tags_input = st.sidebar.text_input("Enter tags (comma-separated):")


TEMP_PDF_DIR = "data/temp_pdfs"
if not os.path.exists(TEMP_PDF_DIR):
    os.makedirs(TEMP_PDF_DIR)

if uploaded_pdfs:
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    with st.spinner("Processing PDFs..."):
        for uploaded_pdf in uploaded_pdfs:
            # Save the uploaded PDF temporarily
            temp_pdf_path = os.path.join(TEMP_PDF_DIR, uploaded_pdf.name)
            with open(temp_pdf_path, 'wb') as f:
                f.write(uploaded_pdf.getbuffer())
            
            # Process and store the PDF with content-based uniqueness
            process_and_store_pdf(temp_pdf_path, tags=tags)

    st.sidebar.success("PDFs have been processed and stored.")

# Sidebar Settings
st.sidebar.header("⚙️ Settings")

# Response Style
response_style = st.sidebar.selectbox("Response Style:", ["Formal", "Informal", "Concise", "Detailed"])

# Language
language = st.sidebar.selectbox("Language:", ["English", "Spanish", "French", "German"])

# Search Filters
st.sidebar.header("🔍 Search Filters")

# Filter by PDF Name
filter_pdf_name = st.sidebar.text_input("Filter by PDF Name:")

# Filter by Tags
filter_tags_input = st.sidebar.text_input("Filter by Tags (comma-separated):")
filter_tags = [tag.strip() for tag in filter_tags_input.split(',')] if filter_tags_input else []

# Prepare filters
filters = {}
if filter_pdf_name:
    filters['pdf_name'] = filter_pdf_name
if filter_tags:
    filters['tags'] = {'$in': filter_tags}

# Summarize PDFs
if st.sidebar.button("Summarize All PDFs"):
    with st.spinner("Generating summary..."):
        summary = summarize_documents()
    st.subheader("📝 Summary of All PDFs")
    st.write(summary)

# Generate Word Cloud
if st.sidebar.button("Generate Word Cloud"):
    with st.spinner("Generating word cloud..."):
        wordcloud_fig = generate_word_cloud()
    st.subheader("🌥️ Word Cloud of PDF Contents")
    st.pyplot(wordcloud_fig)

# Database Inspection
if st.sidebar.button("Show ChromaDB Content"):
    client = get_chroma_client()
    collection = client.get_or_create_collection('pdf_embeddings')
    results = collection.get()
    # Normalize metadata
    metadata_df = pd.json_normalize(results['metadatas'])
    # Create DataFrame
    df = pd.DataFrame({
        'ID': results['ids'],
        'Document': results['documents']
    })
    df = pd.concat([df, metadata_df], axis=1)
    st.subheader("ChromaDB Contents")
    st.dataframe(df)

# Main content area
st.subheader("💬 Ask Questions")
st.write("Choose how you want to ask the question:")
input_choice = st.radio("How would you like to ask your question?", ("Type", "Speak"))
query_input = ""

if input_choice == "Type":
    query_input = st.text_input("Enter your question here:")
    if query_input:
        st.session_state.text_query = query_input

# Handle Voice Input
elif input_choice == "Speak":
    if st.button("Start Recording"):
        st.session_state.voice_query = capture_voice_input()  # Store the voice input in session state

# Retrieve query from session state (either voice or text input)
if input_choice == "Speak":
    query_input = st.session_state.voice_query
elif input_choice == "Type":
    query_input = st.session_state.text_query

# Display the current query to the user if it exists
if query_input:
    st.session_state.current_query = query_input
    st.write(f"**Your question:** {query_input}")

# Retrieve query from session state (either voice or text input)
if input_choice == "Speak":
    query_input = st.session_state.voice_query
elif input_choice == "Type":
    query_input = st.session_state.text_query


print(query_input)

if query_input:
    if st.button("Get Answer"):
        with st.spinner("Searching for the answer..."):
            answer, source_documents = get_answer_conversational(
                query_input,
                st.session_state.chat_history,
                response_style=response_style,
                language=language,
                filters=filters
            )
        # Save the question, answer, and source documents to session state
        st.session_state.conversation.append({
            'question': query_input,
            'answer': answer,
            'source_documents': source_documents
        })
        st.session_state.chat_history.append((query_input, answer))
        st.success("**Answer:**")
        st.write(answer)

                # Generate and Display the Audio for the Answer
        st.session_state.generated_audio_file=generate_audio(answer, language=language)

        # Display the generated MP3 file for the user to play
        print(st.session_state.generated_audio_file)
        
        if st.session_state.generated_audio_file:
            audio_file = open(st.session_state.generated_audio_file, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

        # Display the source PDFs
        st.subheader("📄 Source PDFs:")
        pdf_names = set(
            doc.metadata.get('pdf_name', 'Unknown PDF') for doc in source_documents
        )
        for pdf_name in pdf_names:
            pdf_name_disp = re.sub(r'_[a-f0-9]{8}', '', pdf_name)
            st.write(f"- **{pdf_name_disp}**")
            # pdf_base_name = pdf_name.split('_v')[0]
            # versions = [doc.metadata.get('version', 1) for doc in source_documents if doc.metadata.get('pdf_name') == pdf_name]
            # selected_version = st.selectbox(f"Select version for {pdf_base_name}:", versions, key=f"version_{pdf_base_name}")
            # versioned_pdf_name = f"{pdf_base_name}_v{selected_version}.pdf"
            pdf_path = os.path.join('data/pdfs', pdf_name)
        
            if os.path.exists(pdf_path):
                max_pdf_size = 5 * 1024 * 1024  # 5 MB limit
                pdf_size = os.path.getsize(pdf_path)
                if pdf_size <= max_pdf_size:
                    pdf_name_disp = re.sub(r'_[a-f0-9]{8}', '', pdf_name)
                    
                    with st.expander(f"📖 View {pdf_name_disp}"):
                        # decrypted_pdf = decrypt_pdf(pdf_path)
                        display_pdf(pdf_path)
                else:
                    st.warning(f"{pdf_name} is too large to display. Please download it to view.")
                    decrypted_pdf = decrypt_pdf(pdf_path)
                    b64_pdf = base64.b64encode(decrypted_pdf).decode('utf-8')
                    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{pdf_name}">📥 Download {pdf_name}</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning(f"File {pdf_name} not found.")

            # # Annotations
            # st.subheader(f"✏️ Annotations for {pdf_name}")
            # annotations = load_annotations()
            # existing_annotations = annotations.get(pdf_name, [])
            # st.write("**Existing Annotations:**")
            # for idx, note in enumerate(existing_annotations):
            #     st.write(f"{idx + 1}. {note}")
            # new_annotation = st.text_area(f"Add a new annotation for {pdf_name}:", key=f"annotation_{pdf_name}")
            # if st.button(f"Save Annotation for {pdf_name}", key=f"save_annotation_{pdf_name}"):
            #     save_annotation(pdf_name, new_annotation)
            #     st.success(f"Annotation saved for {pdf_name}.")

        # # AI-Powered Recommendations
        # recommended_pdfs = get_recommendations(query)
        # st.subheader("📚 You might also like:")
        # for pdf in recommended_pdfs:
        #     st.write(f"- {pdf}")
    else:
        pass

# Display conversation history
if st.session_state.conversation:
    st.subheader("📝 Conversation History")
    for idx, qa in enumerate(st.session_state.conversation):
        st.write(f"**Q{idx+1}:** {qa['question']}")
        st.write(f"**A{idx+1}:** {qa['answer']}")
        # Display source PDFs for each QA pair
        pdf_names = set(
            doc.metadata.get('pdf_name', 'Unknown PDF') for doc in qa['source_documents']
        )
        for pdf_name in pdf_names:
            st.write(f"🔗 **Source PDF:** {pdf_name}")

# Generate Report
if st.sidebar.button("Generate Report"):
    report_content = ""
    for idx, qa in enumerate(st.session_state.conversation):
        report_content += f"Q{idx+1}: {qa['question']}\n"
        report_content += f"A{idx+1}: {qa['answer']}\n\n"

    # Export as PDF
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Chatbot Report', ln=True, align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in report_content.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output("chatbot_report.pdf")

    # Provide download link
    with open("chatbot_report.pdf", "rb") as f:
        pdf_bytes = f.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="chatbot_report.pdf">📥 Download Report</a>'
    st.markdown(href, unsafe_allow_html=True)

# Sidebar Help
st.sidebar.header("ℹ️ Help")
st.sidebar.write("""
- **Upload PDFs**: Use the sidebar to upload your PDF documents.
- **Add Tags**: Provide custom tags for your PDFs.
- **Ask Questions**: Type your question in the main area and click 'Get Answer'.
- **View Source PDFs**: After getting an answer, view the source PDFs by expanding them.
- **Annotations**: Add annotations to PDFs.
- **Conversation History**: Scroll down to see your previous questions and answers.
- **Settings**: Customize response style and language.
- **Filters**: Use filters to narrow down your search.
- **Summarization**: Generate summaries of all PDFs.
- **Word Cloud**: Visualize common words in your PDFs.
- **Generate Report**: Export your conversation as a PDF report.
""")

