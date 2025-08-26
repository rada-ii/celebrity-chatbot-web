import streamlit as st
from dotenv import dotenv_values
from openai import OpenAI

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
        color:#191919
    }
    .assistant-message {
        background-color: #f3e5f5;
        margin-right: 20%;
        color: #0f0e2d;
    }
    .sidebar .stSelectbox > div > div {
        background-color: white;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    h1 {
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    @media (max-width: 768px) {
    .chat-message {
        margin-left: 5% !important;
        margin-right: 5% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
env_vars = dotenv_values('.env')
client = OpenAI(api_key=env_vars['OPEN_AI_KEY'])

# Page config
st.set_page_config(
    page_title="Celebrity Chat Bot",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title with better styling
st.markdown("<h1>⭐ Celebrity Chat Experience</h1>", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; color: white; margin-bottom: 2rem;'>
        <p>Chat with your favorite celebrities in a natural, engaging conversation</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with better styling
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")

    famous_person = st.text_input(
        "Celebrity Name",
        value="Elon Musk",
        help="Enter any famous person's name"
    )

    creativity = st.slider(
        "Response Creativity",
        0, 10, 5,
        help="Higher values = more creative responses"
    )

    st.markdown("---")

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation_started = False

    # Start button with better styling
    if not st.session_state.conversation_started:
        if st.button("🚀 Start Conversation", use_container_width=True):
            if famous_person.strip():
                st.session_state.conversation_started = True
                st.session_state.messages = [{
                    "role": "system",
                    "content": [{
                        "type": "input_text",
                        "text": f"You are {famous_person}. Embody their personality, speaking patterns, and viewpoints. Keep responses conversational and engaging while maintaining their authentic voice. Limit responses to 2-3 sentences for natural conversation flow."
                    }]
                }]
                st.rerun()
            else:
                st.error("Please enter a celebrity name")

    # Reset button
    if st.session_state.conversation_started:
        if st.button("🔄 New Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()

        st.markdown("---")
        st.markdown(f"**Currently chatting with:** {famous_person}")

# Main chat area
if st.session_state.conversation_started:
    # Chat container
    chat_container = st.container()

    with chat_container:
        # Display conversation history
        for msg in st.session_state.messages[1:]:  # Skip system message
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {msg['content'][0]['text']}
                </div>
                """, unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>{famous_person}:</strong> {msg['content'][0]['text']}
                </div>
                """, unsafe_allow_html=True)

    # User input at bottom
    user_input = st.chat_input(f"Message {famous_person}...")

    if user_input and user_input.strip():
        # Add user message
        user_msg = {
            "role": "user",
            "content": [{"type": "input_text", "text": user_input}]
        }
        st.session_state.messages.append(user_msg)

        # Get AI response
        try:
            with st.spinner(f"{famous_person} is typing..."):
                response = client.responses.create(
                    model="gpt-3.5-turbo",
                    input=st.session_state.messages,
                    text={"format": {"type": "text"}},
                    reasoning={},
                    tools=[],
                    temperature=float(creativity) / 5,
                    max_output_tokens=2048,
                    top_p=1,
                    store=True,
                    include=[]
                )

                content = response.output[0].content[0].text

                # Add assistant response
                assistant_msg = {
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": content}]
                }
                st.session_state.messages.append(assistant_msg)
                st.rerun()

        except Exception as e:
            st.error(f"Connection error: {e}")

else:
    # Welcome message
    with col2:
        st.markdown("""
        <div style='text-align: center; color: white; padding: 2rem; background-color: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 2rem;'>
            <h3>Ready to start chatting?</h3>
            <p>Choose a celebrity from the sidebar and click "Start Conversation" to begin!</p>
        </div>
        """, unsafe_allow_html=True)