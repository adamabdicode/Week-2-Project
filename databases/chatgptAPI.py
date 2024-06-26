import sqlite3
import os
import openai

def connect_to_database():
    """Connect to the SQLite database."""
    return sqlite3.connect('TriviaData.db')

def fetch_random_question(cursor, difficulty):
    """Fetch a random question of specified difficulty from the database."""
    query = """
    SELECT question_id, question
    FROM questions
    WHERE difficulty = ?
    ORDER BY RANDOM()
    LIMIT 1;
    """
    cursor.execute(query, (difficulty,))
    return cursor.fetchone()

def validate_answer(question, answer):
    """Validate user's answer using OpenAI's ChatGPT model, including the context of the question."""
    openai.api_key = os.getenv('OPENAI_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "I am a trivia validation assistant. I answer questions given to me or validate answers or  trivia game."},
            {"role": "user", "content": f"This is the question or the answer I have: {question}. And this is the question or the answer I want your help validating its correctness: {answer}"}
        ]
    )
    return response['choices'][0]['message']['content']


def update_counter(cursor, question_id):
    """Update the counter each time the question is asked."""
    cursor.execute("UPDATE questions SET count = count + 1 WHERE question_id = ?;", (question_id,))

def update_question_answer(cursor, question_id, answer, connection):
    """Add an answer to the question in the database."""
    cursor.execute("UPDATE questions SET answer = ? WHERE question_id = ?;", (answer, question_id))
    connection.commit()

def main():
    """Main function to run the trivia game."""
    connection = connect_to_database()
    cursor = connection.cursor()
    print_welcome_message()
    manage_game_flow(cursor, connection)
    connection.close()
    print("Exiting the Entertainment Practice Guide Game. Goodbye!")

def print_welcome_message():
    """Print the welcome message for the game."""
    print("Welcome to the Entertainment Practice Guide Game!")

def manage_game_flow(cursor, connection):
    """Handle the main flow of the game."""
    while True:
        choice = prompt_menu()
        if choice == '1':
            handle_trivia_question(cursor, connection)
        elif choice == '2':
            custom_question_workflow(cursor, connection)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def prompt_menu():
    """Display menu and return user's choice."""
    print("\nMenu:")
    print("1. Practice with a question from the trivia database")
    print("2. Enter your own question")
    print("3. Exit")
    return input("Enter your choice (1/2/3): ")

def handle_trivia_question(cursor, connection):
    """Handle fetching and responding to a trivia question."""
    print("Choose difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    difficulty_choice = input("Enter your choice (1/2/3): ")
    try:
        difficulty_map = {1: 'easy', 2: 'medium', 3: 'hard'}
        difficulty = difficulty_map[int(difficulty_choice)]
        question_data = fetch_random_question(cursor, difficulty)
        if question_data:
            question_id, question = question_data
            print(f"\nQuestion: {question}")
            update_counter(cursor, question_id)
            handle_question_response(cursor, question_id, question, connection)
        else:
            print(f"No questions available in the {difficulty} category.")
    except ValueError:
        print("Invalid difficulty. Please choose 1, 2, or 3.")

def handle_question_response(cursor, question_id, question, connection):
    """Handle the response loop for each question."""
    while True:
        user_answer = input("Your answer: ")
        validation_status, validated_answer = validate_answer(question, user_answer)
        print(f"AI's response: {validated_answer}")

        # Check for validation status to manage the response accordingly
        if validation_status == "correct":
            print("Congratulations! That's the correct answer.")
            update_question_answer(cursor, question_id, user_answer, connection)
            break
        elif validation_status == "incorrect":
            print("That's not correct. Try again or type 'skip' to move to another question.")
        elif validation_status == "incomplete":
            print("Please provide a clearer or more complete answer. Type 'skip' if you'd like to move to another question.")

        # Allow user to skip this question if they cannot provide a valid answer
        if user_answer.lower() == "skip":
            break

def custom_question_workflow(cursor, connection):
    """Workflow for entering and handling a custom question."""
    user_question = input("Enter your question: ")
    cursor.execute("INSERT INTO questions (difficulty, question) VALUES (?, ?);", ('custom', user_question))
    connection.commit()
    question_id = cursor.lastrowid
    validated_answer = validate_answer(user_question, "What is the answer to this question?")
    print(f"AI's response: {validated_answer}")
    update_question_answer(cursor, question_id, validated_answer, connection)

if __name__ == "__main__":
    main()
