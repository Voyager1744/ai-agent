from typing import Any


class Memory:
    def __init__(self, max_messages: int = 10):
        self.messages: list[dict[str, str | Any]] = []
        self.max_messages = max_messages

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get(self):
        return self.messages
