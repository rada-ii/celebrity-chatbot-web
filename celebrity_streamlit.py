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
        background-color: #0e1117;
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
    .stChatInputContainer {
        position: sticky;
        bottom: 0;
        background-color: #0e1117;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Get API key
api_key = st.secrets.get("OPEN_AI_KEY")
if not api_key:
    st.error("API key not found. Please check your secrets configuration.")
    st.stop()

# Function to call OpenAI API with streaming simulation
@st.cache_data(show_spinner=False)
def call_openai_api(messages_json, temperature, max_tokens):
    """Cache API calls to prevent unnecessary requests"""
    messages = json.loads(messages_json)
    
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
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Title
st.markdown("# ⭐ Celebrity Chat Experience")

# Sidebar
with st.sidebar:
    st.markdown("### Chat Settings")
    
    famous_person = st.text_input("Celebrity Name", value="Elon Musk")
    creativity = st.slider("Creativity", 0, 10, 5)
    
    if not st.session_state.conversation_started:
        if st.button("Start Conversation", type="primary"):
            if famous_person.strip():
                st.session_state.conversation_started = True
                st.session_state.messages = [{
                    "role": "system",
                    "content": f"You are {famous_person}. Act as this person would, but keep responses conversational and to 2-3 sentences. Be engaging and stay in character."
                }]
                st.rerun()
    
    if st.session_state.conversation_started:
        st.markdown(f"**Currently chatting with:** {famous_person}")
        if st.button("🔄 New Conversation", type="secondary"):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.session_state.processing = False
            st.rerun()

# Main chat interface
if st.session_state.conversation_started:
    # Create container for messages
    chat_container = st.container()
    
    with chat_container:
        # Display all messages except system message
        for i, msg in enumerate(st.session_state.messages[1:], 1):
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
    
    # Show processing indicator
    if st.session_state.processing:
        with st.spinner(f"{famous_person} is typing..."):
            st.empty()
    
    # Chat input - sempre visível
    prompt = st.chat_input("Type your message here...", disabled=st.session_state.processing)
    
    # Process new message
    if prompt and not st.session_state.processing:
        # Set processing flag
        st.session_state.processing = True
        
        # Add user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Rerun to show user message and spinner
        st.rerun()
    
    # Process AI response if we have a new user message and we're processing
    if (st.session_state.processing and 
        len(st.session_state.messages) > 1 and 
        st.session_state.messages[-1]["role"] == "user"):
        
        try:
            # Prepare messages for API call
            messages_json = json.dumps(st.session_state.messages)
            
            # Call OpenAI API
            with st.spinner(f"{famous_person} is thinking..."):
                content = call_openai_api(
                    messages_json,
                    float(creativity) / 5,
                    1000
                )
            
            # Add AI response
            st.session_state.messages.append({"role": "assistant", "content": content})
            
            # Reset processing flag
            st.session_state.processing = False
            
            # Rerun to show AI response
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.processing = False
            st.rerun()

else:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 🎭 Ready to start chatting?
        
        **How it works:**
        1. Enter a celebrity name in the sidebar
        2. Adjust creativity level (higher = more creative responses)
        3. Click 'Start Conversation' 
        4. Begin chatting!
        
        **Try chatting with:**
        - Elon Musk
        - Albert Einstein  
        - Shakespeare
        - Steve Jobs
        - Or anyone else you can think of!
        """)
