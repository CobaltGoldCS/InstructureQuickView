from dataclasses import dataclass
import datetime


@dataclass
class Assignment:
    identifier: int
    name: str
    dueDate: datetime.datetime


