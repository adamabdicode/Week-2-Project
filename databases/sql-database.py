import sqlite3
import random
import openai
import os

# Function to connect to the SQLite database
def connect_to_database():
    return sqlite3.connect('TriviaData.db')

# Function to fetch a random question of specified difficulty from the database
def fetch_random_question(cursor, difficulty):
    query = "SELECT question_id, question FROM questions WHERE difficulty = ? ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(query, (difficulty,))
    row = cursor.fetchone()
    if row:
        question_id, question = row
        return question_id, question
    else:
        return None, None

# Function to validate user's answer using OpenAI's ChatGPT model
def validate_answer(answer):
    openai.api_key = os.getenv('OPENAI_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are validating a user's answer."},
            {"role": "user", "content": answer}
        ]
    )
    return response['choices'][0]['message']['content']

# Function to update the counter for correct answers
def update_counter(cursor, question_id):
    query = "UPDATE counter SET count = count + 1 WHERE question_id = ?;"
    cursor.execute(query, (question_id,))
    connection.commit()

# Function to add an answer to the question in the database
def update_question_answer(cursor, question_id, answer):
    query = "UPDATE questions SET answer = ? WHERE question_id = ?;"
    cursor.execute(query, (answer, question_id))
    connection.commit()

# Main function to run the practice guide game
def main():
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    print("Welcome to the Entertainment Practice Guide Game!")

    while True:
        print("\nMenu:")
        print("1. Practice with a question from the trivia database")
        print("2. Enter your own question")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            difficulty = input("Choose difficulty (Easy/Medium/Hard): ").capitalize()
            question_id, question = fetch_random_question(cursor, difficulty)
            
            if question_id and question:
                print(f"\nQuestion: {question}")
                user_answer = input("Your answer: ")
                
                # Validate user's answer using OpenAI
                validated_answer = validate_answer(user_answer)
                print(f"AI's response: {validated_answer}")

                # Update the question with the validated answer
                update_question_answer(cursor, question_id, validated_answer)
                
                # Update counter for correct answers
                update_counter(cursor, question_id)
            else:
                print(f"No {difficulty} questions available in the database.")
            
            choice = input("\nDo you want to go to the beginning (1) or exit (3)? Enter (1/3): ")
        
        elif choice == '2':
            user_question = input("Enter your question: ")
            
            # Add user's question to the database
            query = "INSERT INTO questions (difficulty, question) VALUES (?, ?);"
            cursor.execute(query, ('Custom', user_question))
            connection.commit()

            # Validate user's question using OpenAI
            validated_answer = validate_answer(user_question)
            print(f"AI's response: {validated_answer}")

            # Get the question_id of the newly inserted question
            question_id = cursor.lastrowid

            # Update the newly inserted question with the validated answer
            update_question_answer(cursor, question_id, validated_answer)

            choice = input("\nDo you want to go to the beginning (1) or exit (3)? Enter (1/3): ")

        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # Close the database connection
    connection.close()
    print("Exiting the Entertainment Practice Guide Game. Goodbye!")

if __name__ == "__main__":
    main()
