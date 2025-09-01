from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLM(ABC):
    @abstractmethod
    async def acomplete(
        self,
        messages: List[Dict[str, str]],
        tools: list[dict] | None = None,
        tool_choose: str = "auto",
    ) -> dict[str, Any]: ...
