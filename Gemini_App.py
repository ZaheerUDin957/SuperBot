import streamlit as st
import google.generativeai as genai
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

def get_google_api_key():
    """
    Get Google API key from user input in the sidebar.
    """
    return st.sidebar.text_input("Enter Google API Key:", type="password")

def configure_genai(api_key):
    """
    Configure the Google Generative AI with the provided API key.
    """
    genai.configure(api_key=api_key)

def get_gemini_response(question):
    """
    Get response from the Gemini model.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text if response else "No response from the model."

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
    st.title("Start Conversation with Gemini")
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

def GeminiBot():
    """
    Main function to run the Gemini chatbot.
    """
    initialize_session_state()

    api_key = get_google_api_key()
    if not api_key:
        st.warning("Please enter your Google API key in the sidebar.")
        return

    configure_genai(api_key)

    st.text_input('YOU: ', key='prompt_input', on_change=submit)

    if st.session_state.entered_prompt != "":
        user_query = st.session_state.entered_prompt
        st.session_state.past.append(user_query)

        with st.spinner("Generating..."):
            ai_response = get_gemini_response(user_query)
        
        st.session_state.generated.append(ai_response)

    display_chat()

