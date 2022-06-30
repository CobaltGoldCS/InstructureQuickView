from dataclasses import dataclass
from datetime import datetime


@dataclass
class Assignment:
    identifier: int
    name: str
    dueDate: datetime


