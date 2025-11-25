import json
import pathlib
from typing import List, Optional
from .models import Park, Visit

DATA_PATH = pathlib.Path(__file__).parent / "data.json"


def _read_data() -> dict:
    if not DATA_PATH.exists():
        return {"parks": [], "visits": []}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_data(data: dict):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_PATH.with_suffix('.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    tmp.replace(DATA_PATH)


def init_db():
    # create file if missing
    if not DATA_PATH.exists():
        _write_data({"parks": [], "visits": []})


def add_park(name: str, state: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None, source_id: Optional[str] = None, notes: Optional[str] = None) -> Park:
    p = Park.create(name=name, state=state, lat=lat, lon=lon, source_id=source_id, notes=notes)
    data = _read_data()
    data['parks'].append({
        'id': p.id,
        'name': p.name,
        'state': p.state,
        'lat': p.lat,
        'lon': p.lon,
        'source_id': p.source_id,
        'notes': getattr(p, 'notes', None),
        'created_at': p.created_at,
    })
    _write_data(data)
    return p


def update_park(park_id: str, **fields) -> Optional[Park]:
    data = _read_data()
    changed = False
    for r in data.get('parks', []):
        if r.get('id') == park_id:
            for k, v in fields.items():
                if k in ('name', 'state', 'lat', 'lon', 'source_id', 'notes'):
                    r[k] = v
                    changed = True
            break
    if changed:
        _write_data(data)
        return find_park_by_id(park_id)
    return None


def list_parks() -> List[Park]:
    data = _read_data()
    parks = []
    for r in sorted(data.get('parks', []), key=lambda x: x.get('name', '')):
        parks.append(Park(id=r['id'], name=r['name'], state=r.get('state'), lat=r.get('lat'), lon=r.get('lon'), source_id=r.get('source_id'), notes=r.get('notes'), created_at=r.get('created_at')))
    return parks


def find_park_by_name(name: str) -> Optional[Park]:
    data = _read_data()
    for r in data.get('parks', []):
        if r.get('name') == name:
            return Park(id=r['id'], name=r['name'], state=r.get('state'), lat=r.get('lat'), lon=r.get('lon'), source_id=r.get('source_id'), notes=r.get('notes'), created_at=r.get('created_at'))
    return None


def find_park_by_id(park_id: str) -> Optional[Park]:
    data = _read_data()
    for r in data.get('parks', []):
        if r.get('id') == park_id:
            return Park(id=r['id'], name=r['name'], state=r.get('state'), lat=r.get('lat'), lon=r.get('lon'), source_id=r.get('source_id'), notes=r.get('notes'), created_at=r.get('created_at'))
    return None


def add_visit(park_id: str, trail: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None, party_size: int = 1, notes: Optional[str] = None) -> Visit:
    v = Visit.create(park_id=park_id, trail=trail, start=start, end=end, party_size=party_size, notes=notes)
    data = _read_data()
    data['visits'].append({
        'id': v.id,
        'park_id': v.park_id,
        'trail': v.trail,
        'start': v.start,
        'end': v.end,
        'party_size': v.party_size,
        'notes': v.notes,
        'created_at': v.created_at,
    })
    _write_data(data)
    return v


def list_visits(park_id: Optional[str] = None) -> List[Visit]:
    data = _read_data()
    visits = []
    rows = data.get('visits', [])
    if park_id:
        rows = [r for r in rows if r.get('park_id') == park_id]
    rows = sorted(rows, key=lambda x: x.get('created_at', ''), reverse=True)
    for r in rows:
        visits.append(Visit(id=r['id'], park_id=r['park_id'], trail=r.get('trail'), start=r.get('start'), end=r.get('end'), party_size=r.get('party_size', 1), notes=r.get('notes'), created_at=r.get('created_at')))
    return visits


def get_visited_park_ids() -> set:
    """Return a set of park IDs that have at least one visit recorded."""
    data = _read_data()
    ids = set()
    for v in data.get('visits', []):
        pid = v.get('park_id')
        if pid:
            ids.add(pid)
    return ids


def clear_visits():
    """Remove all visit records from the store."""
    data = _read_data()
    if 'visits' in data:
        data['visits'] = []
        _write_data(data)


def clear_parks():
    """Remove all parks and visits from the store (complete park reset)."""
    data = _read_data()
    data['parks'] = []
    data['visits'] = []
    _write_data(data)


def clear_all():
    """Remove all stored data (parks, visits) and recreate empty structure."""
    _write_data({"parks": [], "visits": []})


def export_json(path: str):
    data = _read_data()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
