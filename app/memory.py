
class ConversationMemory:

    def __init__(self, max_messages=10):
        self.conversations = {}
        self.max_messages = max_messages

    def add_message(self, conversation_id, role, content):

        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append({
            "role": role,
            "content": content
        })

        # Keep only the latest messages
        self.conversations[conversation_id] = (
            self.conversations[conversation_id][-self.max_messages:]
        )

    def get_history(self, conversation_id):

        return self.conversations.get(conversation_id, [])

    def clear_history(self, conversation_id):

        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
