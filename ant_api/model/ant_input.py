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

    # def __init__(self, finding_date: date, thorax_color: Color, paunch_color: Color, length: int, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.finding_date = finding_date
    #     self.thorax_color = thorax_color
    #     self.paunch_color = paunch_color
    #     self.length = length
