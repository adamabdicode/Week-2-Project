import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from chatgptAPI import (
    connect_to_database,
    fetch_random_question,
    validate_answer,
    update_counter,
    update_question_answer
)

class TriviaGameTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a mock database connection
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE questions (
                               question_id INTEGER PRIMARY KEY,
                               question TEXT,
                               difficulty TEXT,
                               answer TEXT,
                               count INTEGER DEFAULT 0)''')
        self.cursor.execute("INSERT INTO questions (question, difficulty) VALUES ('What is the capital of France?', 'easy')")
        self.cursor.execute("INSERT INTO questions (question, difficulty) VALUES ('What is the largest planet?', 'medium')")
        self.connection.commit()

    def tearDown(self):
        # Close the database connection
        self.connection.close()

    def test_connect_to_database(self):
        connection = connect_to_database()
        self.assertIsInstance(connection, sqlite3.Connection)
        connection.close()

    def test_fetch_random_question(self):
        question = fetch_random_question(self.cursor, 'easy')
        self.assertEqual(question[1], 'What is the capital of France?')

    @patch('openai.ChatCompletion.create')
    @patch('os.getenv')
    def test_validate_answer(self, mock_getenv, mock_openai):
        mock_getenv.return_value = 'fake_api_key'
        mock_openai.return_value = {
            'choices': [{'message': {'content': 'Correct answer'}}]
        }
        response = validate_answer('What is the capital of France?', 'Paris')
        self.assertEqual(response, 'Correct answer')

    def test_update_counter(self):
        question_id = 1
        update_counter(self.cursor, question_id)
        self.cursor.execute("SELECT count FROM questions WHERE question_id = ?", (question_id,))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_update_question_answer(self):
        question_id = 1
        new_answer = 'Paris'
        update_question_answer(self.cursor, question_id, new_answer, self.connection)
        self.cursor.execute("SELECT answer FROM questions WHERE question_id = ?", (question_id,))
        answer = self.cursor.fetchone()[0]
        self.assertEqual(answer, new_answer)

if __name__ == '__main__':
    unittest.main()
