from tasks3 import ParkTracker
import os

# Helper to clean up after tests
def cleanup():
    if os.path.exists("parks.json"):
        os.remove("parks.json")

# Test adding a park
def test_add_park():
    tracker = ParkTracker()
    tracker.parks = []
    tracker.add_park("Test Park", "CA")  # Valid state code
    assert any(p["name"] == "Test Park" for p in tracker.parks)
    cleanup()

# Test listing parks
def test_list_parks(capsys):
    tracker = ParkTracker()
    tracker.parks = [{"name": "Park A", "state": "NY", "visited": False, "notes": []}]  # Valid state
    tracker.list_parks()
    captured = capsys.readouterr()
    assert "Park A" in captured.out
    cleanup()

# Test marking a park visited
def test_mark_visited():
    tracker = ParkTracker()
    tracker.parks = [{"name": "Park B", "state": "TX", "visited": False, "notes": []}]  # Valid state
    tracker.mark_visited("Park B")
    assert tracker.parks[0]["visited"] is True
    cleanup()

# Test adding a note
def test_add_note():
    tracker = ParkTracker()
    tracker.parks = [{"name": "Park C", "state": "AZ", "visited": False, "notes": []}]  # Valid state
    tracker.add_note("Park C", "Beautiful place")
    assert "Beautiful place" in tracker.parks[0]["notes"]
    cleanup()

