import pytest
from core.agent import Agent


@pytest.mark.asyncio
async def test_datetime_tool():
    agent = Agent()
    reply = await agent.ask("Какое сегодня число?")
    assert any(
        word in reply.lower()
        for word in [
            "202",
            "январ",
            "феврал",
            "март",
            "апрел",
            "май",
            "июн",
            "июл",
            "авг",
            "сент",
            "окт",
            "ноябр",
            "декабр",
        ]
    )


@pytest.mark.asyncio
async def test_chain_tools():
    agent = Agent()
    reply = await agent.ask("Сколько будет год сейчас умножить на 2?")
    # ожидаем что ответ будет числом, близким к 4040 (если сейчас 2025)
    numbers = [int(s) for s in reply.split() if s.isdigit()]
    assert numbers, f"Ответ должен содержать число, а пришло: {reply}"


@pytest.mark.asyncio
async def test_unknown_tool_handling():
    agent = Agent()
    # Подсовываем LLM запрос к несуществующему инструменту
    # (Мы имитируем это вручную через системное сообщение, чтобы протестить поведение)
    agent.memory.add("assistant", None)  # очистка истории
    reply = await agent.ask("Вызови инструмент с названием test_tool")
    assert "error" in reply.lower()
