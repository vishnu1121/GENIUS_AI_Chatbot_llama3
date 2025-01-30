import sqlite3
from functools import lru_cache
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template = """
🌟 *GENIUS Activated* 🌟  

Hello, User! I am **GENIUS** (General Expert Navigator for Intelligent User Support), powered by **Llama 3**.  
I’m here to assist you with tasks, answer your questions, and provide smart solutions for whatever you need.  

Here’s what I can do, thanks to Llama 3’s advanced capabilities:  
1. I can process nuanced, multi-part questions and provide detailed, context-aware answers.  
2. From math equations to coding challenges, I can break down problems step by step.  
3. I can write stories, poems, jokes, or even help brainstorm ideas in any style or tone.  
4. I can understand and respond in numerous languages, making communication seamless.     
5. I can analyze data, summarize text, or offer tailored recommendations based on your input.  

Let’s get started! Here’s the context of our conversation so far:  
{context}  

Your last input: {user_input}  

What can I help you with today? (Ask me anything, or let’s chat!) 
"""


model = OllamaLLM(model="llama3", base_url="http://localhost:11434")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model



def setup_database():
    """Sets up the SQLite database and creates the history table if it doesn't exist."""
    conn = sqlite3.connect("conversation_history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, role TEXT, message TEXT)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_id ON history (id)")
    conn.commit()
    return conn, cursor



@lru_cache(maxsize=200)
def get_recent_messages(cursor):
    """Retrieves the most recent 100 messages from the database."""
    cursor.execute("SELECT role, message FROM history ORDER BY id DESC LIMIT 100")
    return cursor.fetchall()


def add_message(conn, cursor, role, message):
    """Adds a new message to the database and updates the cache."""
    cursor.execute("INSERT INTO history (role, message) VALUES (?, ?)", (role, message))
    conn.commit()
    get_recent_messages.cache_clear()  # Clear the cache to refresh recent messages


def format_context(messages):
    """Formats the conversation history into a string for the template."""
    return "\n".join([f"{role}: {message}" for role, message in messages])



class ChatbotConfig:
    def __init__(self, default_context_length=5):
        self.default_context_length = default_context_length
        self.current_context_length = default_context_length  # Start with the default value

    def set_context_length(self, length):
        """Manually set context length."""
        self.current_context_length = length

    def adjust_context_based_on_complexity(self, user_input):
        """Adjust context length based on conversation complexity."""
        # Example of complexity detection based on input length
        complexity_score = len(user_input.split())
        if complexity_score > 20:  # Complex input
            self.set_context_length(10)  # Increase context length for complex input
        elif complexity_score > 10:  # Medium complexity
            self.set_context_length(7)
        else:  # Simple input
            self.set_context_length(self.default_context_length)


def conversation():
    """
    Main conversation loop to interact with the Genius chatbot.
    - Initializes the SQLite database.
    - Handles user input and maintains context.
    - Stores user and chatbot interactions in the database.
    - Gracefully exits on user request.
    """
    conn, cursor = setup_database()
    print("Hi, I'm Genius. How can I help you? Type 'quit' if you want to exit.")


    chatbot_config = ChatbotConfig(default_context_length=5)

    while True:
        user_input = input("You: ")


        if user_input.lower() == "quit":
            print("Genius: Goodbye! Have a great day!")
            break

        try:

            chatbot_config.adjust_context_based_on_complexity(user_input)


            add_message(conn, cursor, "User", user_input)


            recent_messages = get_recent_messages(cursor)[-chatbot_config.current_context_length:]


            context = format_context(recent_messages)


            result = chain.invoke({"context": context, "user_input": user_input})
            print("Genius:", result)

            add_message(conn, cursor, "Genius", result)

        except Exception as e:
            print(f"Error occurred: {e}. Ensure that the Ollama server is running and accessible.")
            break


    cursor.close()
    conn.close()



conversation()

# Workflow of the Program and Chatbot:

# 1. **Program Initialization:**
#    - The program starts by setting up the SQLite database with a table to store conversation history.
#    - The `ChatbotConfig` class is instantiated to manage the dynamic context length of the chatbot based on conversation complexity.

# 2. **Conversation Loop:**
#    - The chatbot prompts the user with "Hi, I'm Genius. How can I help you? Type 'quit' if you want to exit."
#    - The program enters an infinite loop to handle user inputs and responses.

# 3. **User Input Handling:**
#    - The program waits for the user input via `input("You: ")`.
#    - If the user types 'quit', the chatbot ends the conversation and exits the loop.
#    - Otherwise, the user's input is processed.

# 4. **Adjusting Context Length Dynamically:**
#    - The chatbot checks the complexity of the user input using the `adjust_context_based_on_complexity` method.
#    - Based on the length of the user's input, the context length is adjusted:
#       - For complex inputs (longer than 20 words), the context length is increased (e.g., 10 messages).
#       - For medium complexity (10-20 words), the context length is set to 7.
#       - For simple inputs (less than 10 words), the default context length is used (e.g., 5).

# 5. **Adding User Message to Database:**
#    - The user's message is added to the SQLite database and the cache is updated.
#    - The `add_message` function stores the user's message and clears the cache to refresh the recent message list.

# 6. **Retrieving Recent Messages:**
#    - The program queries the SQLite database to fetch the most recent messages based on the adjusted context length.
#    - It retrieves a limited number of recent messages as per the `chatbot_config.current_context_length` (which is dynamically set).

# 7. **Formatting Context for Response:**
#    - The recent messages are formatted into a string that will be used as the context for generating a response. This ensures the chatbot uses the relevant context to provide a better, more coherent answer.

# 8. **Generating Response with Llama 3:**
#    - The `chain.invoke()` function is called with the formatted context and the user's input to generate a response using the Llama 3 model.
#    - The response from the model is then printed to the screen as the chatbot's reply.

# 9. **Adding Chatbot Response to Database:**
#    - The chatbot's response is stored in the SQLite database.
#    - The response is also cached to allow quick retrieval of recent conversation history.

# 10. **Error Handling:**
#    - If any errors occur (such as issues connecting to the Ollama server), an error message is displayed, and the loop ends.

# 11. **Graceful Exit:**
#    - When the user types 'quit', the program prints "Goodbye! Have a great day!" and closes the database connection before exiting.

# 12. **End of Conversation:**
#    - The program gracefully exits after the conversation ends, ensuring that the database connection is properly closed.

#Thank you