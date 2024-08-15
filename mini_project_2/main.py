import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from google.api_core.exceptions import GoogleAPIError

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Sidebar content
st.sidebar.title("Chat Settings")
bot_personality = st.sidebar.selectbox(
    "Choose bot personality:",
    ("Friendly", "Professional", "Humorous", "Casual")
)

font_size = st.sidebar.slider(
    "Adjust font size of responses:",
    min_value=10, max_value=40, value=20
)

st.sidebar.markdown("Adjust the chatbot's settings from here!")

# Fetch Google API Key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    st.error("API key is not set. Please check your environment variables.")
else:
    # Set up Google Gemini-Pro AI model
    try:
        gen_ai.configure(api_key=GOOGLE_API_KEY)
        model = gen_ai.GenerativeModel('gemini-pro')
    except GoogleAPIError as e:
        st.error(f"Failed to configure Google Generative AI: {e}")
        st.stop()

    # Function to translate roles between Gemini-Pro and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        return "assistant" if user_role == "model" else user_role

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        try:
            st.session_state.chat_session = model.start_chat(history=[])
        except GoogleAPIError as e:
            st.error(f"Failed to start chat session: {e}")
            st.stop()

    # Display the chatbot's title on the page
    st.title("🤖 Gemini Pro - ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(
                f"<div style='font-size:{font_size}px;'>{message.parts[0].text}</div>",
                unsafe_allow_html=True
            )

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro...")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        try:
            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)

            # Apply the bot's personality to the response (you can define how it behaves based on selection)
            response_text = gemini_response.text
            if bot_personality == "Friendly":
                response_text = f"😊 {response_text}"
            elif bot_personality == "Professional":
                response_text = f"🔧 {response_text}"

            # Display Gemini-Pro's response with selected font size
            with st.chat_message("assistant"):
                st.markdown(
                    f"<div style='font-size:{font_size}px;'>{response_text}</div>",
                    unsafe_allow_html=True
                )
        except GoogleAPIError as e:
            st.error(f"Failed to send message to Gemini-Pro: {e}")
