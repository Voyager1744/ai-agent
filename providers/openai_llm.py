from core.llm import BaseLLM
from core.config import settings
from openai import AsyncOpenAI


class OpenAILLM(BaseLLM):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def acomplete(self, messages, tools=None, tool_choice="auto"):
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
