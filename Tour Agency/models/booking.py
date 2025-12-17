from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List
from .client import Client, Traveler
from .resort import Resort

@dataclass
class FlightInfo:
    from_city: str
    to_city: str
    departure: datetime
    arrival: datetime
    pnr: str

@dataclass
class HotelInfo:
    name: str
    address: str
    stars: int

@dataclass
class PaymentInfo:
    method: str
    masked_pan: str
    transaction_id: str
    approved: bool

@dataclass
class Booking:
    booking_id: str
    client: Client
    travelers: List[Traveler]
    resort: Resort
    start_date: date
    end_date: date
    flight: FlightInfo
    hotel: HotelInfo
    total_price_uah: int
    payment: PaymentInfo
    created_at: datetime = field(default_factory=datetime.now)
