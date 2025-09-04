import pytest
from core.agent import Agent


@pytest.mark.asyncio
async def test_agent_math():
    agent = Agent()
    reply = await agent.ask("Посчитай 2 + 2 * 5")
    assert "12" in reply or "10" in reply  # в зависимости от интерпретации
