import psycopg2
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a PostgreSQL connection
connection = psycopg2.connect(
    host='your_host',
    port='your_port',
    database='your_database',
    user='your_username',
    password='your_password'
)

# Create a chatbot instance
chatbot = ChatBot('DatabaseChatBot')

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

# Define a function to process user input and generate a response
def get_response(user_input):
    db_response = None

    # Check if user input requires a database query
    if 'query' in user_input.lower():
        # Extract the query from user input
        query = user_input.split('query')[1].strip()

        # Execute the user's query
        db_response = execute_query(query)

    # Generate a response using the chatbot
    response = chatbot.get_response(user_input)

    # Construct the final response
    if db_response:
        final_response = f"Database Response: {db_response}\nChatBot Response: {response}"
    else:
        final_response = str(response)

    return final_response

# Example usage
while True:
    user_input = input("User: ")

    # Get the response
    response = get_response(user_input)

    # Print the response
    print("Bot:", response)
