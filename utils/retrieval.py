# utils/retrieval.py
import streamlit as st
from utils.chroma_manager import get_chroma_client
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma 
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

def get_retriever(filters=None):
    client = get_chroma_client()
    collection_name = 'pdf_embeddings'
    embeddings = OpenAIEmbeddings()  #
    # retriever = collection.as_retriever(search_type="mmr", search_kwargs={"k":5})
    vectorstore = Chroma(collection_name=collection_name, embedding_function=embeddings, client=client)
    
    # Now you can use as_retriever()
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k":1})

    if filters:
        retriever.search_kwargs['filter'] = filters
    return retriever

@st.cache_data(show_spinner=False)
# utils/retrieval.py
def get_answer_conversational(query, chat_history, response_style="Formal", language="English", filters=None):
    # Define the retriever
    retriever = get_retriever(filters)

    # Initialize the language model (LLM)
    llm = OpenAI()

    # Initialize the ConversationalRetrievalChain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Get the result from the conversation chain
    result = conversation_chain({
        'question': query,
        'chat_history': chat_history
    })

    # Extract the answer and source documents
    answer = result['answer']
    source_documents = result['source_documents']

    return answer, source_documents