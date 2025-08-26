import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Celebrity Chat Bot",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .chat-message {
        padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message { background-color: #e3f2fd; margin-left: 20%; color:#191919; }
    .assistant-message { background-color: #f3e5f5; margin-right: 20%; color: #0f0e2d; }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white; border: none; border-radius: 20px;
        padding: 0.5rem 2rem; font-weight: bold;
    }
    h1 { color: white; text-align: center; margin-bottom: 2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    @media (max-width: 768px) {
        .chat-message { margin-left: 5% !important; margin-right: 5% !important; }
    }
</style>
""", unsafe_allow_html=True)

# Get API key
api_key = st.secrets.get("OPEN_AI_KEY")
if not api_key:
    st.error("API key not found. Please check your secrets configuration.")
    st.stop()

# Function to call OpenAI API directly
def call_openai_api(messages, temperature, max_tokens):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error: {response.status_code}")

# Main title
st.markdown("<h1>⭐ Celebrity Chat Experience</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    
    famous_person = st.text_input("Celebrity Name", value="Elon Musk")
    creativity = st.slider("Response Creativity", 0, 10, 5)
    
    st.markdown("---")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation_started = False
    
    # Start conversation
    if not st.session_state.conversation_started:
        if st.button("🚀 Start Conversation", use_container_width=True):
            if famous_person.strip():
                st.session_state.conversation_started = True
                st.session_state.messages = [{
                    "role": "system",
                    "content": f"You are {famous_person}. Embody their personality, speaking patterns, and viewpoints. Keep responses conversational and engaging while maintaining their authentic voice. Limit responses to 2-3 sentences for natural conversation flow."
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

# Main chat interface
if st.session_state.conversation_started:
    # Display conversation history
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>{famous_person}:</strong> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # User input
    user_input = st.chat_input(f"Message {famous_person}...")
    
    if user_input and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        try:
            with st.spinner(f"{famous_person} is typing..."):
                content = call_openai_api(
                    st.session_state.messages,
                    float(creativity) / 5,
                    2048
                )
                
                st.session_state.messages.append({"role": "assistant", "content": content})
                st.rerun()
                
        except Exception as e:
            st.error(f"Connection error: {e}")

else:
    # Welcome screen
    st.markdown("""
    <div style='text-align: center; color: white; padding: 2rem; background-color: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 2rem;'>
        <h3>Ready to start chatting?</h3>
        <p>Choose a celebrity from the sidebar and click "Start Conversation" to begin!</p>
    </div>
    """, unsafe_allow_html=True)
