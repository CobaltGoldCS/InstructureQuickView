from dataclasses import dataclass
from datetime import datetime


@dataclass
class Assignment:
    identifier: int
    name: str
    dueDate: datetime

@dataclass
class User:
    utoken: str
    domain: str


