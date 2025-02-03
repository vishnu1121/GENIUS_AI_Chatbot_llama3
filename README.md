# GENIUS_AI_Chatbot_llama3
GENIUS is a conversational AI chatbot powered by Llama 3, designed to assist users with tasks, answer questions, and provide intelligent recommendations. It stores conversation history in an SQLite database, dynamically adjusts context length, and offers context-aware responses for seamless interaction.

# Features:

1)Maintains a stateful conversation by storing all messages in an SQLite database.  
2)Utilizes Python's `lru_cache` to quickly retrieve recent messages, enhancing performance.  
3)Modifies the conversation context length based on the complexity of user inputs, ensuring relevant and informed responses.  
4)Interfaces with the Llama 3 model via the Ollama API using LangChain’s prompt templating, enabling robust and flexible AI responses.
