# Celebrity Chat Bot

AI-powered web application for realistic conversations with celebrities.

## Live Demo
🌐 [Chat with Celebrities](https://celebrity-chatbot-web.streamlit.app)
*(Link will be active after deployment)*

## Features
- Natural conversation with any celebrity
- Personality-accurate responses
- Adjustable creativity levels
- Modern responsive web interface
- Real-time chat experience

## Technology Stack
- Python 3.8+
- OpenAI GPT API
- Streamlit web framework
- Custom CSS styling

## Local Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/celebrity-chatbot-web.git
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
This is a learning project. Feel free to fork and experiment.

## License
MIT License - feel free to use for educational purposes.