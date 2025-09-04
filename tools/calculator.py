from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Математическое выражение")


class CalculatorTool:
    name = "calculator"
    description = "Вычисляет математическое выражение"
    schema = CalculatorInput.model_json_schema()

    async def run(self, payload: CalculatorInput) -> str:
        try:
            result = eval(payload.expression, {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"Ошибка вычисления: {e}"
