from dotenv import dotenv_values
from openai import OpenAI

env_vars = dotenv_values('.env')
client = OpenAI(api_key=st.secrets['OPEN_AI_KEY'])

# Celebrity name validation
while True:
    famous_person = input("What celebrity person would you like to talk to?\n").strip()
    if famous_person:
        break
    else:
        print("Please enter a celebrity name.")

# Initial question validation
while True:
    initial_prompt = input(f"Ok! Now ask {famous_person} a question!\n").strip()
    if initial_prompt:
        break
    else:
        print("Please enter a question.")

# Creativity validation
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

messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "input_text",
                "text": f"You are {famous_person}. Embody their personality, speaking patterns, and viewpoints. Keep responses conversational and engaging while maintaining their authentic voice. Limit responses to 2-3 sentences for natural conversation flow."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": initial_prompt
            }
        ]
    }
]

while True:
    try:
        response = client.responses.create(
            model="gpt-3.5-turbo",
            input=messages,
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[],
            temperature=creativity_num,
            max_output_tokens=2048,
            top_p=1,
            store=True,
            include=[]
        )

        content = response.output[0].content[0].text

        messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": content
                }
            ]
        })

        print(f"\n{famous_person}: {content}\n")

        # User response validation
        while True:
            prompt = input(f'Respond to {famous_person} (or type "bye" to exit): ').strip()
            if prompt:
                break
            else:
                print("Please enter a response or type 'bye' to exit.")

        if prompt.lower() == "bye":
            print("Thanks for chatting!")
            break

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt
                }
            ]
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again.")
        continue
