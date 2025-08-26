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

# Simple dark theme CSS
st.markdown("""
<style>
    .stApp { 
        background-color: #1a1a1a;
    }
    .chat-message {
        padding: 1rem; 
        border-radius: 10px; 
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .user-message { 
        background-color: #2d3748;
        color: white;
        margin-left: 10%;
    }
    .assistant-message { 
        background-color: #4a5568;
        color: white;
        margin-right: 10%;
    }
    h1 { 
        color: white; 
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Get API key
api_key = st.secrets.get("OPEN_AI_KEY")
if not api_key:
    st.error("API key not found. Please check your secrets configuration.")
    st.stop()

# Function to call OpenAI API
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

# Initialize session state ONLY ONCE
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False

# Title
st.markdown("# ⭐ Celebrity Chat Experience")

# Sidebar
with st.sidebar:
    st.markdown("### Chat Settings")
    
    famous_person = st.text_input("Celebrity Name", value="Elon Musk")
    creativity = st.slider("Creativity", 0, 10, 5)
    
    if not st.session_state.conversation_started:
        if st.button("Start Conversation"):
            if famous_person.strip():
                st.session_state.conversation_started = True
                st.session_state.messages = [{
                    "role": "system",
                    "content": f"You are {famous_person}. Keep responses to 2-3 sentences."
                }]
                st.rerun()
    
    if st.session_state.conversation_started:
        if st.button("New Conversation"):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()

# Chat interface
if st.session_state.conversation_started:
    # Display messages
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
    
    # Input field
    prompt = st.chat_input("Your message...")
    
    # KRITIČNA PROMENA: Process input bez st.rerun()
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        try:
            content = call_openai_api(
                st.session_state.messages,
                float(creativity) / 5,
                1000
            )
            st.session_state.messages.append({"role": "assistant", "content": content})
            # REMOVED st.rerun() - ovo je uzrok infinity loop-a
            
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.markdown("### Ready to start chatting?")
    st.markdown("Choose a celebrity from the sidebar and click 'Start Conversation'")
