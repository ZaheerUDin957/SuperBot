from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


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

def get_openai_api_key():
    """
    Get OpenAI API key from user input in the sidebar.
    """
    return st.sidebar.text_input("Enter OpenAI API Key:", type="password")

def initialize_chat_model(api_key):
    """
    Initialize the ChatOpenAI model.
    """
    return ChatOpenAI(
        temperature=0.5,
        model_name="gpt-3.5-turbo",
        openai_api_key=api_key,
        max_tokens=1
    )

def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    system_message_content = """
        your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.

        1. Greet the user politely ask user name and ask how you can assist them with AI-related queries.
        2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learning, natural language processing, computer vision, and related topics.
        3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
        4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
        5. Be patient and considerate when responding to user queries, and provide clear explanations.
        6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
        7. Do Not generate the long paragarphs in response. Maximum Words should be 100.

        Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being.
    """
    zipped_messages = [SystemMessage(content=system_message_content)]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages

def generate_response(chat_model):
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat_model(zipped_messages)

    return ai_response.content

def submit():
    """
    Define function to submit user input.
    """
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""

def display_chat():
    """
    Display the chat history.
    """
    st.title("Start a Conversation with OpenAI 🤖")
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            # Display AI response
            message(st.session_state["generated"][i], key=str(i))
            # Display user message
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

def openAiBot():
    """
    Main function to run the OpenAI chatbot.
    """
    initialize_session_state()

    api_key = get_openai_api_key()
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
        return

    chat_model = initialize_chat_model(api_key)
    
    # Create a text input for user
    st.text_input('YOU: ', key='prompt_input', on_change=submit)

    if st.session_state.entered_prompt != "":
        # Get user query
        user_query = st.session_state.entered_prompt

        # Append user query to past queries
        st.session_state.past.append(user_query)

        # Generate response
        output = generate_response(chat_model)

        # Append AI response to generated responses
        st.session_state.generated.append(output)

    display_chat()


