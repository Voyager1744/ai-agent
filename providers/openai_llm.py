from openai import AsyncOpenAI
from core.config import settings


class OpenAILLM:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def acomplete(self, messages, tools=None, tool_choice=None):
        response = await self.client.chat.completions.create(
            model=settings.model_gpt,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
