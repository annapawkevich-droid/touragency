from dataclasses import dataclass

@dataclass
class Traveler:
    first_name: str
    last_name: str
    card_id: str

@dataclass
class Client(Traveler):
    phone: str
    email: str
