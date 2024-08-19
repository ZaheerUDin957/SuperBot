import streamlit as st
import requests
from itertools import zip_longest
from streamlit_chat import message

def initialize_session_state():
    """
    Initialize session state variables.
    """
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []  # Store AI generated responses

    if 'past' not in st.session_state:
        st.session_state['past'] = []  # Store past user inputs

    if 'entered_prompt' not in st.session_state:
        st.session_state['entered_prompt'] = ""  # Store the latest user input

def get_huggingface_api_key():
    """
    Get Hugging Face API key from user input in the sidebar.
    """
    return st.sidebar.text_input("Enter Hugging Face API Key:", type="password")

def generate_text(prompt, api_key, model_url="https://api-inference.huggingface.co/models/gpt2", max_length=50):
    """
    Generate text from a given prompt using the Hugging Face API.
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length
        }
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    response = requests.post(model_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text']
    else:
        return f"Error {response.status_code}: {response.text}"

def build_message_list():
    """
    Build a list of past and generated messages.
    """
    messages = []
    for user_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if user_msg is not None:
            messages.append({'role': 'user', 'content': user_msg})
        if ai_msg is not None:
            messages.append({'role': 'ai', 'content': ai_msg})
    return messages

def submit():
    """
    Submit user input.
    """
    st.session_state.entered_prompt = st.session_state.prompt_input
    st.session_state.prompt_input = ""

def display_chat():
    """
    Display the chat history.
    """
    st.title("Start Conversation with HuggingFace🤖")
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

def HuggingFaceBot():
    """
    Main function to run the Hugging Face chatbot.
    """
    initialize_session_state()

    api_key = get_huggingface_api_key()
    if not api_key:
        st.warning("Please enter your Hugging Face API key in the sidebar.")
        return

    st.text_input('YOU: ', key='prompt_input', on_change=submit)

    if st.session_state.entered_prompt != "":
        user_query = st.session_state.entered_prompt
        st.session_state.past.append(user_query)

        with st.spinner("Generating..."):
            ai_response = generate_text(user_query, api_key)
        
        st.session_state.generated.append(ai_response)

    display_chat()


