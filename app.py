import streamlit as st
from OpenAi_App import openAiBot
from HuggingFace_App import HuggingFaceBot
from Gemini_App import GeminiBot
from Langchain_App import LangchainBot
# from LLamaindex_App import llamaindexBot
from styles import overall_css

st.set_page_config(page_title="SuperBot 🤖", page_icon="🤖", layout="wide")
# Apply the CSS styles
st.markdown(overall_css, unsafe_allow_html=True)

st.title("SuperBot Application 🤖")
st.subheader('Elevating Chat Experiences with Integrated AI Technologies 🌟')

# Initialize session state for page navigation with "openai" as the default
if "page" not in st.session_state:
    st.session_state.page = "openai"

def navigate_to(page):
    st.session_state.page = page

# Create columns for navigation buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("OpenAI Bot"):
        navigate_to("openai")

with col2:
    if st.button("HuggingFace Bot"):
        navigate_to("huggingface")

with col3:
    if st.button("Gemini Bot"):
        navigate_to("gemini")

with col4:
    if st.button("Langchain Bot"):
        navigate_to("langchain")

# with col5:
#     if st.button("LlamaIndex Bot"):
#         navigate_to("llamaindex")

# Display the appropriate page based on session state
if st.session_state.page == "openai":
    openAiBot()
elif st.session_state.page == "huggingface":
    HuggingFaceBot()
elif st.session_state.page == "gemini":
    GeminiBot()
elif st.session_state.page == "langchain":
    LangchainBot()
# elif st.session_state.page == "llamaindex":
#     llamaindexBot()
else:
    openAiBot()  # Default to OpenAI Bot

