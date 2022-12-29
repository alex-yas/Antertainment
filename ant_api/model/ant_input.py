from pydantic import BaseModel
from enum import Enum
from datetime import date


class Color(str, Enum):
    BLACK = "BLACK"
    YELLOW = "YELLOW"
    BROWN = "BROWN"
    NO_INFO = "NO_INFO"


class AntInput(BaseModel):
    finding_date: date
    thorax_color: Color
    paunch_color: Color
    length: int
