import json
from providers.openai_llm import OpenAILLM
from core.promts import SYSTEM_PROMPT
from core.memory import Memory
from tools.calculator import CalculatorTool, CalculatorInput
from tools.datetime_tool import DatetimeTool, DatetimeInput


class Agent:
    def __init__(self):
        self.llm = OpenAILLM()
        self.memory = Memory()
        self.tools = {
            "calculator": CalculatorTool(),
            "datetime_tool": DatetimeTool(),
        }

    async def ask(self, user_message: str) -> str:
        # сохраняем сообщение пользователя
        self.memory.add("user", user_message)

        # список инструментов для LLM (только первый вызов!)
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

        # сообщения: system + вся история
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.memory.get()

        # первый запрос с инструментами
        response = await self.llm.acomplete(messages, tools=tools)
        msg = response.choices[0].message

        # цикл — пока LLM вызывает инструменты
        while msg.tool_calls:
            # сохраняем assistant с tool_calls
            messages.append(msg.model_dump(exclude_none=True))

            for call in msg.tool_calls:
                tool = self.tools[call.function.name]
                args = json.loads(call.function.arguments)
                result = await tool.run(self._parse_input(tool, args))

                # добавляем ответ инструмента
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result,
                    }
                )

            # новый запрос без tools
            response = await self.llm.acomplete(messages)
            msg = response.choices[0].message

        # сохраняем ответ ассистента в память
        self.memory.add("assistant", msg.content)
        return msg.content

    def _parse_input(self, tool, args: dict):
        """Парсинг аргументов под конкретный инструмент"""
        if isinstance(tool, CalculatorTool):
            return CalculatorInput(**args)
        if isinstance(tool, DatetimeTool):
            return DatetimeInput(**args)
        return args
