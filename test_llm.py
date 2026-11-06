

from app.memory import ConversationMemory
from app.llm_client import generate_response

memory = ConversationMemory(max_messages=10)

chat_id = "test_001"

# First message
message1 = "My name is Nandu."

response1 = generate_response(
    memory.get_history(chat_id),
    message1
)

memory.add_message(chat_id, "user", message1)
memory.add_message(chat_id, "assistant", response1)

print("User:", message1)
print("Bot:", response1)

# Second message
message2 = "What is my name?"

response2 = generate_response(
    memory.get_history(chat_id),
    message2
)

memory.add_message(chat_id, "user", message2)
memory.add_message(chat_id, "assistant", response2)

print("\nUser:", message2)
print("Bot:", response2)

print("\nTotal messages:", len(memory.get_history(chat_id)))
