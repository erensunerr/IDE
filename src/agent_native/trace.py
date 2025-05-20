from dataclasses import dataclass
from typing import Any

@dataclass
class Trace:
    tool: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    def to_dict(self):
        return {"tool": self.tool, "args": self.args, "kwargs": self.kwargs}
