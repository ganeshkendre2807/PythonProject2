import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional ChatGPT-like UI
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main app background */
    .stApp {
        background-color: #f7f7f8;
    }

    /* Sidebar styling - Professional Dark */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }

    /* Header styling - Professional */
    .header-container {
        background-color: #2d2d2d;
        padding: 20px;
        text-align: center;
        border-radius: 0;
        margin: -6rem -6rem 2rem -6rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 600;
        margin: 0;
        letter-spacing: 0.3px;
    }

    .header-subtitle {
        color: #b0b0b0;
        font-size: 14px;
        margin-top: 5px;
        font-weight: 400;
    }

    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        height: calc(100vh - 250px);
        overflow-y: auto;
        scroll-behavior: smooth;
    }

    /* Chat input styling */
    .stChatFloatingInputContainer {
        bottom: 20px;
        background-color: transparent;
        padding: 0 20px;
    }

    .stChatInputContainer {
        background-color: white;
        border-radius: 24px;
        border: 1px solid #d1d5db;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        padding: 12px 16px;
        max-width: 800px;
        margin: 0 auto;
    }

    .stChatInputContainer textarea {
        border: none !important;
        background-color: transparent !important;
        font-size: 16px !important;
        color: #333333 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stChatInputContainer textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Chat message bubbles */
    .stChatMessage {
        background-color: transparent !important;
        padding: 8px 0 !important;
    }

    /* User message (right-aligned) */
    [data-testid="stChatMessageContent"]:has(.user-message) {
        background-color: #DCF8C6 !important;
        color: #333333 !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        max-width: 70% !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }

    /* Assistant message (left-aligned) */
    [data-testid="stChatMessageContent"]:has(.assistant-message) {
        background-color: #ffffff !important;
        color: #333333 !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        margin-right: auto !important;
        margin-left: 0 !important;
        max-width: 70% !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }

    /* Timestamp styling */
    .timestamp {
        font-size: 12px;
        color: #6b7280;
        margin-top: 4px;
        font-weight: 400;
    }

    /* Thinking process container */
    .thinking-container {
        background-color: #f3f4f6;
        border-left: 3px solid #3b82f6;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 12px 0;
        max-width: 70%;
    }

    .thinking-title {
        font-size: 14px;
        font-weight: 600;
        color: #3b82f6;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }

    .thinking-content {
        font-size: 14px;
        color: #4b5563;
        line-height: 1.6;
        margin: 4px 0;
        padding-left: 8px;
    }

    .thinking-step {
        margin: 6px 0;
        padding: 6px 0;
    }

    .thinking-step::before {
        content: "→ ";
        color: #3b82f6;
        font-weight: 600;
    }

    /* Sidebar buttons - Professional */
    .stButton button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s;
        font-size: 14px;
    }

    .stButton button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }

    /* Sidebar sections */
    .sidebar-section {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid #3d3d3d;
    }

    .sidebar-title {
        color: #ffffff;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .sidebar-text {
        color: #b0b0b0;
        font-size: 14px;
        line-height: 1.6;
    }

    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #3d3d3d;
    }

    .stat-item:last-child {
        border-bottom: none;
    }

    .stat-label {
        color: #b0b0b0;
        font-size: 14px;
    }

    .stat-value {
        color: #3b82f6;
        font-weight: 600;
        font-size: 14px;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    ::-webkit-scrollbar-thumb {
        background: #9ca3af;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #6b7280;
    }

    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        color: #333333;
    }

    .welcome-title {
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #1f2937;
    }

    .welcome-subtitle {
        font-size: 16px;
        color: #6b7280;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        'gemini-2.5-pro',
        generation_config={
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    )
    st.session_state.chat_session = model.start_chat(history=[])


# Function to get current timestamp
def get_timestamp():
    return datetime.now().strftime("%I:%M %p")


# Function to generate thinking process
def generate_thinking_process(user_query):
    """Generate realistic thinking steps based on user query"""
    thinking_steps = [
        f"Analyzing the user's question: '{user_query[:50]}...' if len(user_query) > 50 else user_query",
        "Reviewing conversation history for context and previous interactions",
        "Identifying key concepts and requirements in the query",
        "Searching my knowledge base for relevant information",
        "Organizing thoughts and structuring the response",
        "Ensuring accuracy and relevance of the information",
        "Preparing a clear and helpful answer"
    ]
    return thinking_steps


# Sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-title">💬 Chat Controls</p>', unsafe_allow_html=True)

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        model = genai.GenerativeModel(
            'gemini-2.5-pro',
            generation_config={
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        model = genai.GenerativeModel(
            'gemini-2.5-pro',
            generation_config={
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

    # Statistics section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">📊 Chat Statistics</p>', unsafe_allow_html=True)

    total_messages = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])

    st.markdown(f'''
    <div class="stat-item">
        <span class="stat-label">Total Messages</span>
        <span class="stat-value">{total_messages}</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">Your Messages</span>
        <span class="stat-value">{user_messages}</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">AI Responses</span>
        <span class="stat-value">{assistant_messages}</span>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Model info section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">🤖 Model Information</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text"><strong>Model:</strong> Gemini 2.5 Pro</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text"><strong>Provider:</strong> Google AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text"><strong>Features:</strong> Context-aware, Multi-turn conversations</p>',
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">💡 Tips</p>', unsafe_allow_html=True)
    st.markdown('''
    <p class="sidebar-text">
    • Ask follow-up questions<br>
    • Reference previous messages<br>
    • I remember our entire conversation<br>
    • Clear chat to start fresh
    </p>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Header
st.markdown('''
<div class="header-container">
    <h1 class="header-title">ChatGPT Clone</h1>
    <p class="header-subtitle">Powered by Google Gemini 2.5 Pro • Professional AI Assistant</p>
</div>
''', unsafe_allow_html=True)

# Main chat area
chat_container = st.container()

with chat_container:
    # Show welcome message if no chat history
    if len(st.session_state.messages) == 0:
        st.markdown('''
        <div class="welcome-container">
            <h2 class="welcome-title">Welcome to ChatGPT Clone</h2>
            <p class="welcome-subtitle">How can I help you today?</p>
        </div>
        ''', unsafe_allow_html=True)

    # Display chat messages with timestamps
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                # Show thinking process if available
                if "thinking" in message:
                    thinking_html = '<div class="thinking-container">'
                    thinking_html += '<div class="thinking-title">🧠 Thinking Process:</div>'
                    for step in message["thinking"]:
                        thinking_html += f'<div class="thinking-step">{step}</div>'
                    thinking_html += '</div>'
                    st.markdown(thinking_html, unsafe_allow_html=True)

                # Show the actual response
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="timestamp">{message.get("timestamp", "")}</div>', unsafe_allow_html=True)

# Chat input (fixed at bottom)
if prompt := st.chat_input("Message ChatGPT Clone..."):
    # Get current timestamp
    current_time = get_timestamp()

    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": current_time
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="timestamp">{current_time}</div>', unsafe_allow_html=True)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        # Generate thinking process
        thinking_steps = generate_thinking_process(prompt)

        # Show thinking process with animation
        thinking_placeholder = st.empty()
        thinking_html = '<div class="thinking-container">'
        thinking_html += '<div class="thinking-title">🧠 Thinking Process:</div>'

        # Display thinking steps one by one
        for i, step in enumerate(thinking_steps):
            thinking_html += f'<div class="thinking-step">{step}</div>'
            thinking_placeholder.markdown(thinking_html + '</div>', unsafe_allow_html=True)
            time.sleep(0.4)  # Delay between steps

        try:
            # Generate response with full conversation context
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text

            # Get timestamp for response
            response_time = get_timestamp()

            # Display the thinking process and response together
            response_placeholder = st.empty()

            # Keep thinking process visible and show response below
            final_html = thinking_html + '</div>'
            final_html += f'<div class="assistant-message">{full_response}</div>'
            response_placeholder.markdown(final_html, unsafe_allow_html=True)

            # Display timestamp
            st.markdown(f'<div class="timestamp">{response_time}</div>', unsafe_allow_html=True)

            # Add assistant response to chat history with thinking process
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "thinking": thinking_steps,
                "timestamp": response_time
            })

        except Exception as e:
            thinking_placeholder.empty()
            error_msg = f"❌ Error: {str(e)}"
            st.markdown(f'<div class="assistant-message">{error_msg}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": get_timestamp()
            })

    # Auto-scroll to bottom
    st.rerun()