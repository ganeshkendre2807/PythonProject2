import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="A.I.S.H.A",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching ChatGPT UI exactly
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}

    /* Main background - light gray like ChatGPT */
    .stApp {
        background-color: #f9f9f9;
    }

    /* Sidebar - white theme */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        padding: 0;
        border-right: 1px solid #e5e5e5;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Sidebar header with logo */
    .sidebar-header {
        padding: 12px 12px 20px 12px;
        border-bottom: 1px solid #e5e5e5;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #2d2d2d;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    /* New chat button - white theme */
    .stButton > button {
        background-color: transparent;
        color: #2d2d2d;
        border: 1px solid #d1d1d1;
        border-radius: 8px;
        padding: 10px 14px;
        font-weight: 500;
        width: 100%;
        transition: all 0.15s ease;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .stButton > button:hover {
        background-color: #f4f4f4;
        border-color: #b1b1b1;
    }

    /* Chat history items */
    .chat-history {
        padding: 8px 12px;
    }

    .chat-item {
        background-color: transparent;
        color: #2d2d2d;
        padding: 10px 12px;
        margin: 4px 0;
        border-radius: 8px;
        font-size: 14px;
        cursor: pointer;
        transition: background-color 0.15s ease;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .chat-item:hover {
        background-color: #f4f4f4;
    }

    .chat-item.active {
        background-color: #f4f4f4;
    }

    /* Sidebar sections */
    .sidebar-section {
        padding: 12px;
        border-top: 1px solid #e5e5e5;
        margin-top: 8px;
    }

    .sidebar-section-title {
        color: #6e6e6e;
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .sidebar-info {
        color: #2d2d2d;
        font-size: 13px;
        line-height: 1.5;
        margin: 4px 0;
    }

    .sidebar-info strong {
        color: #000;
    }

    /* Main chat area */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0;
    }

    /* Top header bar */
    .top-header {
        position: sticky;
        top: 0;
        background-color: #fff;
        border-bottom: 1px solid #e5e5e5;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 100;
        margin: -6rem -6rem 0 -6rem;
    }

    .model-selector {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #2d2d2d;
        font-size: 15px;
        font-weight: 600;
    }

    .header-actions {
        display: flex;
        gap: 8px;
    }

    /* Chat messages container */
    .chat-messages {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Remove default Streamlit chat styling */
    .stChatMessage {
        background-color: transparent !important;
        padding: 24px 0 !important;
    }

    /* User message styling */
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        padding: 0 !important;
    }

    .user-message-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin: 16px 0;
    }

    .user-message {
        background-color: #f4f4f4;
        color: #2d2d2d;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 70%;
        font-size: 15px;
        line-height: 1.6;
        word-wrap: break-word;
    }

    /* Assistant message styling */
    .assistant-message-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        margin: 16px 0;
    }

    .assistant-message {
        background-color: transparent;
        color: #2d2d2d;
        padding: 12px 0;
        max-width: 100%;
        font-size: 15px;
        line-height: 1.7;
        word-wrap: break-word;
    }

    .assistant-message p {
        margin: 12px 0;
    }

    .assistant-message ul, .assistant-message ol {
        margin: 12px 0;
        padding-left: 24px;
    }

    .assistant-message li {
        margin: 6px 0;
    }

    .assistant-message code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 14px;
    }

    .assistant-message pre {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 16px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 12px 0;
    }

    /* Avatar styling */
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 14px;
        margin-right: 12px;
        flex-shrink: 0;
    }

    .user-avatar {
        background-color: #19c37d;
        color: white;
    }

    .assistant-avatar {
        background-color: #2d2d2d;
        color: white;
    }

    /* Chat input area - matches ChatGPT exactly */
    .stChatFloatingInputContainer {
        background-color: transparent;
        padding: 0 20px 20px 20px;
        bottom: 0;
    }

    .stChatInputContainer {
        background-color: #fff;
        border: 1px solid #d1d1d1;
        border-radius: 24px;
        box-shadow: 0 0 8px rgba(0,0,0,0.06);
        max-width: 800px;
        margin: 0 auto;
        padding: 12px 16px;
    }

    .stChatInputContainer textarea {
        border: none !important;
        background-color: transparent !important;
        font-size: 15px !important;
        color: #2d2d2d !important;
        padding: 0 !important;
        resize: none !important;
    }

    .stChatInputContainer textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Welcome screen */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        text-align: center;
        padding: 40px 20px;
    }

    .welcome-icon {
        font-size: 48px;
        margin-bottom: 20px;
    }

    .welcome-title {
        font-size: 32px;
        font-weight: 600;
        color: #2d2d2d;
        margin-bottom: 12px;
    }

    .welcome-subtitle {
        font-size: 16px;
        color: #6e6e6e;
        margin-bottom: 32px;
    }

    .suggestion-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        max-width: 800px;
        margin: 0 auto;
    }

    .suggestion-card {
        background-color: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.15s ease;
        text-align: left;
    }

    .suggestion-card:hover {
        background-color: #f9f9f9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .suggestion-title {
        font-size: 14px;
        font-weight: 600;
        color: #2d2d2d;
        margin-bottom: 6px;
    }

    .suggestion-text {
        font-size: 13px;
        color: #6e6e6e;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #d1d1d1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #b1b1b1;
    }

    /* Remove gaps */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state with conversation history stack
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history_stack" not in st.session_state:
    st.session_state.chat_history_stack = []

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        'gemini-2.5-pro',
        generation_config={
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    )
    st.session_state.chat_session = model.start_chat(history=[])

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None


# Function to create new chat
def create_new_chat():
    st.session_state.messages = []
    model = genai.GenerativeModel(
        'gemini-2.5-pro',
        generation_config={
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    )
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.current_chat_id = None


# Sidebar
with st.sidebar:
    # Sidebar header with logo
    st.markdown('''
    <div class="sidebar-header">
        <div class="sidebar-logo">
            <span>🤖</span>
            <span>A.I.S.H.A</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # New chat button
    if st.button("✏️ New chat"):
        create_new_chat()
        st.rerun()

    # Chat history
    if len(st.session_state.chat_history_stack) > 0:
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">Recent Chats</div>', unsafe_allow_html=True)

        for idx, chat_preview in enumerate(reversed(st.session_state.chat_history_stack[-10:])):
            chat_title = chat_preview[:40] + "..." if len(chat_preview) > 40 else chat_preview
            st.markdown(f'<div class="chat-item">{chat_title}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Model info section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">About</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="sidebar-info"><strong>A.I.S.H.A</strong> - Your AI Assistant</div>
    <div class="sidebar-info">Context-aware conversations</div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Statistics section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Statistics</div>', unsafe_allow_html=True)

    total_messages = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])

    st.markdown(f'''
    <div class="sidebar-info"><strong>Total Messages:</strong> {total_messages}</div>
    <div class="sidebar-info"><strong>Your Messages:</strong> {user_messages}</div>
    <div class="sidebar-info"><strong>AI Responses:</strong> {assistant_messages}</div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Tips</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="sidebar-info">
    • I remember our entire conversation<br>
    • Ask follow-up questions naturally<br>
    • Reference previous messages<br>
    • Clear chat to start fresh
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Top header
st.markdown('''
<div class="top-header">
    <div class="model-selector">
        <span>A.I.S.H.A</span>
    </div>
</div>
''', unsafe_allow_html=True)

# Main chat container
chat_container = st.container()

with chat_container:
    # Welcome screen
    if len(st.session_state.messages) == 0:
        st.markdown('''
        <div class="welcome-screen">
            <div class="welcome-icon">🤖</div>
            <h1 class="welcome-title">Welcome to A.I.S.H.A</h1>
            <p class="welcome-subtitle">Artificial Intelligence Simulated Humanoid Assistant</p>
        </div>
        ''', unsafe_allow_html=True)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            if message["role"] == "user":
                st.markdown(
                    f'<div class="user-message-container"><div class="user-message">{message["content"]}</div></div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="assistant-message-container"><div class="assistant-message">{message["content"]}</div></div>',
                    unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Message A.I.S.H.A..."):
    # Add to chat history stack
    if prompt not in st.session_state.chat_history_stack:
        st.session_state.chat_history_stack.append(prompt)

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="user-message-container"><div class="user-message">{prompt}</div></div>',
                    unsafe_allow_html=True)

    # Generate assistant response with full conversation context
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()

        try:
            # Send message with full conversation history maintained by Gemini
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text

            # Display response
            message_placeholder.markdown(
                f'<div class="assistant-message-container"><div class="assistant-message">{full_response}</div></div>',
                unsafe_allow_html=True)

            # Add to message history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.markdown(
                f'<div class="assistant-message-container"><div class="assistant-message">{error_msg}</div></div>',
                unsafe_allow_html=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

    st.rerun()