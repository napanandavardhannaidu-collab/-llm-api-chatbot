
import unittest

from app.memory import ConversationMemory


class TestConversationMemory(unittest.TestCase):

    def setUp(self):
        self.memory = ConversationMemory(max_messages=10)

    def test_add_and_retrieve_messages(self):
        self.memory.add_message("chat_001", "user", "Hello")
        self.memory.add_message("chat_001", "assistant", "Hi!")

        history = self.memory.get_history("chat_001")

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Hello")
        self.assertEqual(history[1]["content"], "Hi!")

    def test_conversations_are_isolated(self):
        self.memory.add_message("chat_001", "user", "My name is Nandu")
        self.memory.add_message("chat_002", "user", "My name is Rahul")

        history_one = self.memory.get_history("chat_001")
        history_two = self.memory.get_history("chat_002")

        self.assertEqual(history_one[0]["content"], "My name is Nandu")
        self.assertEqual(history_two[0]["content"], "My name is Rahul")

    def test_maximum_message_limit(self):
        for i in range(12):
            self.memory.add_message("chat_001", "user", f"Message {i}")

        history = self.memory.get_history("chat_001")

        self.assertEqual(len(history), 10)
        self.assertEqual(history[0]["content"], "Message 2")
        self.assertEqual(history[-1]["content"], "Message 11")

    def test_clear_conversation(self):
        self.memory.add_message("chat_001", "user", "Hello")

        self.memory.clear_history("chat_001")

        self.assertEqual(self.memory.get_history("chat_001"), [])

    def test_unknown_conversation(self):
        self.assertEqual(self.memory.get_history("unknown"), [])


if __name__ == "__main__":
    unittest.main()
