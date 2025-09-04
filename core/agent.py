import asyncio
import json
from providers.openai_llm import OpenAILLM
from core.promts import SYSTEM_PROMPT
from core.memory import Memory
from tools.calculator import CalculatorTool, CalculatorInput


class Agent:
    def __init__(self):
        self.llm = OpenAILLM()
        self.memory = Memory()
        self.tools ={
            'calculator': CalculatorTool(),
        }

    async def ask(self, user_message: str) -> str:
        self.memory.add("user", user_message)

        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.schema,
                },
            }
            for tool in self.tools.values()
        ]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.memory.get()

        # 🔹 Первый запрос: с инструментами
        response = await self.llm.acomplete(messages, tools=tools, tool_choice="auto")
        msg = response.choices[0].message

        if msg.tool_calls:
            # 1. Сохраняем ответ ассистента (с tool_calls)
            messages.append(msg.model_dump(exclude_none=True))

            # 2. Выполняем инструменты
            for call in msg.tool_calls:
                tool = self.tools[call.function.name]
                args = json.loads(call.function.arguments)
                result = await tool.run(CalculatorInput(**args))

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result,
                    }
                )

            # 3. Второй запрос — уже без tools
            response = await self.llm.acomplete(messages)
            msg = response.choices[0].message

        self.memory.add("assistant", msg.content)
        return msg.content
