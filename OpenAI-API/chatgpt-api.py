import os
import openai

# Retrieve API key from environment variable
openai.api_key = os.getenv('OPENAI_KEY')

# Specify the model to use and the messages to send
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a university instructor and can explain programming concepts clearly in a few words."},
        {"role": "user", "content": "What are the advantages of pair programming?"}
    ]
)

# Print the response from OpenAI
print(completion['choices'][0]['message']['content'])
