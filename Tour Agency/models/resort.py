from dataclasses import dataclass
from typing import Dict

@dataclass
class SurveyAnswers:
    sea: int
    mountain: int
    excursion: int
    nature: int
    family: int
    party: int

@dataclass
class Resort:
    name: str
    country: str
    profile: Dict[str, int]
    desc: str
