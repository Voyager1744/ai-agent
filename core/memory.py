from typing import Any


class Memory:
    def __init__(self, max_messages: int = 10):
        self.messages: list[dict[str, str | Any]] = []
        self.max_messages = max_messages

    def add(self, role: str, content: str) -> bool:
        """
        Добавляет сообщение в память.
        Возвращает True, если произошло переполнение.
        """
        self.messages.append({"role": role, "content": content})
        return len(self.messages) > self.max_messages

    def trim(self):
        """Обрезает историю, оставляя последние max_messages"""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get(self):
        return self.messages
