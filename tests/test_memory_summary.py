import pytest
import asyncio
from core.agent import Agent

@pytest.mark.asyncio
async def test_memory_summary(monkeypatch):
    agent = Agent()

    # Подменяем summarize, чтобы не тратить токены на реальный запрос
    async def fake_summarize():
        return "Пользователь много говорил о математике и времени."
    monkeypatch.setattr(agent, "summarize", fake_summarize)

    # Генерируем длинный диалог
    for i in range(10):  # больше, чем max_messages
        await agent.ask(f"Сообщение номер {i}")

    # Проверяем, что summary реально сохранилось
    history = agent.memory.get()
    has_summary = any("Краткое резюме" in msg["content"] for msg in history if msg["role"] == "system")

    assert has_summary, "Агент должен сохранять резюме в память при переполнении"
