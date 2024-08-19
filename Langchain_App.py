import streamlit as st
import os
from PyPDF2 import PdfReader
import docx
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from streamlit_chat import message
from langchain.callbacks import get_openai_callback

def LangchainBot():
    load_dotenv()
    st.title("Chat with your files")

    initialize_session_state()

    with st.sidebar:
        uploaded_files = st.file_uploader("Upload your file", type=['pdf', 'docx', 'csv'], accept_multiple_files=True)
        process = st.button("Process")
        openai_api_key = st.text_input("OpenAI API Key", type="password")

    if process:
        handle_file_processing(uploaded_files)

    if st.session_state.processComplete and openai_api_key:
        if st.session_state.vectorstore is None:
            st.error("Vectorstore is not available. Please process the file first.")
        else:
            st.session_state.conversation = get_conversation_chain(st.session_state.vectorstore, openai_api_key)
            st.session_state.apiKeyProvided = True

    if st.session_state.apiKeyProvided:
        user_question = st.chat_input("Ask a question about your files.")
        if user_question:
            handle_user_input(user_question)

def initialize_session_state():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processComplete" not in st.session_state:
        st.session_state.processComplete = None
    if "apiKeyProvided" not in st.session_state:
        st.session_state.apiKeyProvided = False
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

def handle_file_processing(uploaded_files):
    try:
        files_text = get_files_text(uploaded_files)
        st.write("File loaded...")
        text_chunks = get_text_chunks(files_text)
        st.write("File chunks created...")
        vectorstore = get_vectorstore(text_chunks)
        st.write("Vector Store Created...")
        st.session_state.vectorstore = vectorstore
        st.session_state.processComplete = True
        st.write(f"Vectorstore successfully set: {vectorstore is not None}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def get_files_text(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension == ".pdf":
            text += get_pdf_text(uploaded_file)
        elif file_extension == ".docx":
            text += get_docx_text(uploaded_file)
        else:
            text += get_csv_text(uploaded_file)
    return text

def get_pdf_text(pdf):
    pdf_reader = PdfReader(pdf)
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    return text

def get_docx_text(docx_file):
    doc = docx.Document(docx_file)
    text = " ".join([para.text for para in doc.paragraphs])
    return text

def get_csv_text(csv_file):
    # Placeholder function to handle CSV text extraction
    return "CSV text processing not implemented."

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=900,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    knowledge_base = FAISS.from_texts(text_chunks, embeddings)
    return knowledge_base

def get_conversation_chain(vectorstore, openai_api_key):
    if vectorstore is None:
        st.error("The vectorstore is not initialized.")
        return None
    try:
        llm = ChatOpenAI(openai_api_key=openai_api_key, model_name='gpt-3.5-turbo', temperature=0, max_tokens=1)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        st.error(f"An error occurred while creating the conversation chain: {e}")
        return None

def handle_user_input(user_question):
    try:
        with get_openai_callback() as cb:
            response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        response_container = st.container()
        with response_container:
            for i, messages in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    message(messages.content, is_user=True, key=str(i))
                else:
                    message(messages.content, key=str(i))
    except Exception as e:
        st.error(f"An error occurred during conversation: {e}")


