# Celebrity Chat Bot

AI-powered web application for realistic conversations with celebrities.

## Live Demo
🌐 [Chat with Celebrities](https://celebrity-chatbot.streamlit.app/)


## Features
- Natural conversation with any celebrity
- Personality-accurate responses
- Adjustable creativity levels
- Modern responsive web interface
- Real-time chat experience

## Technology Stack
- Python + Streamlit
- OpenAI GPT-3.5-turbo API
- Native Streamlit chat components

## Local Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/rada-ii/celebrity-chatbot-web.git
cd celebrity-chatbot-web
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in project root:
```
OPEN_AI_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
streamlit run celebrity_streamlit.py
```

5. Open your browser to `http://localhost:8501`

## Usage
1. Enter celebrity name in sidebar
2. Adjust creativity level (0-10)
3. Click "Start Conversation"
4. Begin chatting naturally

## Project Structure
```
celebrity-chatbot-web/
├── celebrity_streamlit.py    # Main Streamlit web application
├── celebrity_terminal.py     # Terminal version for testing
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── .env                     # API keys (not in repo)
```

## Contributing
Feel free to fork and experiment with this learning project.

## License
MIT License - feel free to use for educational purposes.
