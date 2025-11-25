from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
import uuid


def new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Park:
    id: str
    name: str
    state: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    source_id: Optional[str]
    notes: Optional[str]
    created_at: str

    @staticmethod
    def create(name: str, state: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None, source_id: Optional[str] = None, notes: Optional[str] = None) -> 'Park':
        return Park(id=new_id(), name=name, state=state, lat=lat, lon=lon, source_id=source_id, notes=notes, created_at=datetime.utcnow().isoformat())


@dataclass
class Visit:
    id: str
    park_id: str
    trail: Optional[str]
    start: Optional[str]
    end: Optional[str]
    party_size: int
    notes: Optional[str]
    created_at: str

    @staticmethod
    def create(park_id: str, trail: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None, party_size: int = 1, notes: Optional[str] = None) -> 'Visit':
        return Visit(id=new_id(), park_id=park_id, trail=trail, start=start, end=end, party_size=party_size, notes=notes, created_at=datetime.utcnow().isoformat())
