import psycopg2
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement

# Create a PostgreSQL connection
connection = psycopg2.connect(
    host='your_host',
    port='your_port',
    database='your_database',
    user='your_username',
    password='your_password'
)

# Create a chatbot instance
chatbot = ChatBot('PGSQLBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot using an English corpus
trainer.train('chatterbot.corpus.english')

# Define a function to execute SQL queries and retrieve responses
def execute_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def get_response(input_text):
    user_input = Statement(input_text)
    response = chatbot.generate_response(user_input)
    return response.text

# Example usage
while True:
    user_input = input("User: ")

    # Execute the user's query
    db_response = execute_query(user_input)

    if db_response:
        print("Database: ", db_response)
    else:
        response = get_response(user_input)
        print("ChatBot: ", response)
