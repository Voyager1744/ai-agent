from datetime import datetime
from pydantic import BaseModel


class DatetimeInput(BaseModel):
    format: str = "%Y-%m-%d %H:%M:%S"


class DatetimeTool:
    name = "datetime_tool"
    description = "Возвращает текущее время в заданном формате"
    schema = DatetimeInput.model_json_schema()

    async def run(self, args: DatetimeInput) -> str:
        return datetime.now().strftime(args.format)
