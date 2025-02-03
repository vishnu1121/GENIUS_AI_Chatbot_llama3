# GENIUS_AI_Chatbot_llama3
GENIUS is a conversational AI chatbot powered by Llama 3, designed to assist users with tasks, answer questions, and provide intelligent recommendations. It stores conversation history in an SQLite database, dynamically adjusts context length, and offers context-aware responses for seamless interaction.

# Features

1)Maintains a stateful conversation by storing all messages in an SQLite database.  
2)Utilizes Python's `lru_cache` to quickly retrieve recent messages, enhancing performance.  
3)Modifies the conversation context length based on the complexity of user inputs, ensuring relevant and informed responses.  
4)Interfaces with the Llama 3 model via the Ollama API using LangChain’s prompt templating, enabling robust and flexible AI responses.


# Prerequisites
Python 3.7  
An active API server (such as Ollama) accessible at your chosen endpoint.  
Required Python packages as specified in the `requirements.txt` file.

# Installation  
Clone the Repository
```bash
   git clone https://github.com/yourusername/genius-ai-chatbot.git
   cd genius-ai-chatbot
```
## Downloading Llama 3 from Ollama
- Navigate to the [Ollama website](https://ollama.ai) and go to the "Download" or "Get Started" section.
- Download and install the Ollama application for your operating system.
- Open the Ollama application, search for "Llama 3" in the Models or Marketplace section, and click "Download" or "Install" to add it to your available models.
- Confirm that Llama 3 is installed and ready to be used in your project.

## Code Structure
main.py: The main script containing the chatbot logic, database setup, and conversation loop.

Prompt Template: The chatbot uses a customizable template to generate responses (Use AI for unique templates). The template is defined in the template variable.

# Database Functions:

setup_database(): Initializes the SQLite database and creates the history table if it doesn't exist.  
get_recent_messages(): Retrieves the most recent messages from the database.  
add_message(): Adds a new message to the database and updates the cache.

# Context Management:  
The ChatbotConfig class manages the context length and adjusts it based on the complexity of user input.

# Customization
Prompt Template: You can modify the template variable in the script to change the chatbot's greeting and capabilities.  
Context Length: Adjust the default_context_length in the ChatbotConfig class to control how much conversation history the chatbot considers.  
Model: You can switch to a different model by changing the model parameter in the OllamaLLM initialization. Choose your own model depending on your specifications of your PC or running host.

# Troubleshooting  
Ollama Server Not Running: Ensure the Ollama server is running and accessible.If not, start the server and try again.  
Database Issues: If the database becomes corrupted or inaccessible, delete the conversation_history.db file and restart the chatbot to create a new database.

## Future extensions (some of them might be complex to design):  
Enhanced Context Complexity Analysis: The current method in adjust_context_based_on_complexity uses a simple word count. We can consider more advanced natural language processing techniques to assess the complexity of the conversation.

Scalability of Cached Messages: The LRU cache is limited to 200 calls, which is fine for a small-scale application. For larger-scale or long-running applications, I might need to implement a more sophisticated caching or message retrieval strategy.

Multi-Model Support: Integrating support for additional language models or API providers (e.g., OpenAI's GPT, Cohere, Anthropic) and allow users to switch between them.

Advanced NLP Features: Add sentiment analysis, named entity recognition, or intent detection to better understand and respond to user queries.

Frontend Integration: Develop a web-based interface using frameworks like React, Vue, or Angular to provide a more interactive and visually appealing experience.

Voice Integration: Incorporate speech-to-text and text-to-speech functionalities for a voice-enabled chatbot.

Third-Party API Integrations: Integrate with external services such as:
- Weather APIs: to provide weather updates.
- News APIs: to fetch the latest headlines.
- Calendar/Scheduling APIs: to set reminders or schedule events.

Authentication and Authorization: Implement user accounts, login systems, and session management to personalize conversations.

User Profiles and History: Store individual conversation histories per user and allow for profile customization and personalized responses.

Feedback and Learning: Incorporate mechanisms for users to provide feedback, helping the chatbot learn and improve its responses over time.

# Contributing  
Contributions are welcome! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request.  
This chatbot needs customizations :)

