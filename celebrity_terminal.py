from dotenv import dotenv_values
from openai import OpenAI

# Load environment variables from .env file
env_vars = dotenv_values('.env')
api_key = env_vars.get('OPEN_AI_KEY')

# Check if API key is available
if not api_key:
    print("API key not found. Please check your .env file.")
    exit()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Celebrity name input validation
while True:
    famous_person = input("What celebrity person would you like to talk to?\n").strip()
    if famous_person:
        break
    else:
        print("Please enter a celebrity name.")

# Initial question input validation
while True:
    initial_prompt = input(f"Ok! Now ask {famous_person} a question!\n").strip()
    if initial_prompt:
        break
    else:
        print("Please enter a question.")

# Creativity level input validation
while True:
    creativity = input("How creative do you want the responses to be (on scale 0-10)?\n").strip()
    try:
        creativity_float = float(creativity)
        if 0 <= creativity_float <= 10:
            creativity_num = creativity_float / 5
            break
        else:
            print("Please enter a number between 0 and 10.")
    except ValueError:
        print("Please enter a valid number between 0 and 10.")

# Initialize conversation with system and user messages
messages = [
    {
        "role": "system",
        "content": f"You are {famous_person}. Embody their personality, speaking patterns, and viewpoints. Keep responses conversational and engaging while maintaining their authentic voice. Limit responses to 2-3 sentences for natural conversation flow."
    },
    {
        "role": "user",
        "content": initial_prompt
    }
]

# Main conversation loop
while True:
    try:
        # Call OpenAI Chat Completions API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=creativity_num,
            max_tokens=2048
        )

        # Extract response content
        content = response.choices[0].message.content

        # Add assistant response to conversation history
        messages.append({
            "role": "assistant",
            "content": content
        })

        # Display celebrity response
        print(f"\n{famous_person}: {content}\n")

        # Get user response with validation
        while True:
            prompt = input(f'Respond to {famous_person} (or type "bye" to exit): ').strip()
            if prompt:
                break
            else:
                print("Please enter a response or type 'bye' to exit.")

        # Check for exit command
        if prompt.lower() == "bye":
            print("Thanks for chatting!")
            break

        # Add user response to conversation history
        messages.append({
            "role": "user",
            "content": prompt
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again.")
        continue
