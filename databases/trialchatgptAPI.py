import sqlite3
import os
import openai

# Connect to the SQLite database
connection = sqlite3.connect('TriviaData.db')
cursor = connection.cursor()

# Fetch data from the database where answers are missing
query = "SELECT question_id, difficulty, question FROM questions WHERE answer IS NULL;"
cursor.execute(query)
rows = cursor.fetchall()

# Retrieve the OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_KEY')

# Prepare the system message
system_message = {"role": "system", "content": "You are a university instructor and can explain programming concepts clearly in a few words."}

# Loop through each question and get the answer from OpenAI
for row in rows:
    question_id, difficulty, question = row
    messages = [
        system_message,
        {"role": "user", "content": question}
    ]
    
    # Connect to OpenAI and send the messages
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    # Extract the answer
    answer = completion['choices'][0]['message']['content']
    
    # Print the question and the corresponding answer
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print("-" * 50)
    
    # Update the database with the answer
    update_query = "UPDATE questions SET answer = ? WHERE question_id = ?"
    cursor.execute(update_query, (answer, question_id))
    connection.commit()

# Close the database connection
connection.close()
