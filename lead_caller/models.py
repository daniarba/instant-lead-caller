"""Data models shared by the flow, adapters and CLI."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Lead:
    name: str
    phone: str
    source: str = "web_form"
    submitted_at: Optional[str] = None

    def as_dict(self) -> dict:
        return {"name": self.name, "phone": self.phone, "source": self.source,
                "submitted_at": self.submitted_at}


@dataclass
class CallResult:
    connected: bool
    answers: dict = field(default_factory=dict)
    duration_s: float = 0.0
    transcript: list = field(default_factory=list)
