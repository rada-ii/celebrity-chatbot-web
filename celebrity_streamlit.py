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

# Get API key
api_key = st.secrets.get("OPEN_AI_KEY")
if not api_key:
    st.error("API key not found. Please check your secrets configuration.")
    st.stop()

# Function to call OpenAI API
def call_openai_api(messages, temperature, max_tokens):
    """Call OpenAI API"""
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
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# Title
st.title("⭐ Celebrity Chat Experience")

# Sidebar
with st.sidebar:
    st.header("Chat Settings")
    
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
        st.write(f"**Currently chatting with:** {famous_person}")
        if st.button("🔄 New Conversation", type="secondary"):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()

# Main chat interface
if st.session_state.conversation_started:
    
    # Display chat messages using Streamlit's built-in chat elements
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(f"**{famous_person}:** {message['content']}")
    
    # Accept user input
    if prompt := st.chat_input("What would you like to ask?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner(f"{famous_person} is thinking..."):
                try:
                    response = call_openai_api(
                        st.session_state.messages,
                        float(creativity) / 5,
                        1000
                    )
                    st.write(f"**{famous_person}:** {response}")
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {e}")
                    # Remove the user message if API call failed
                    st.session_state.messages.pop()

else:
    # Welcome screen
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
