from typing import Optional, List, Dict

class InputData:
    def __init__(
        self,
        transcript: str,
        location: Dict[str, float],
        location_history: List[Dict[str, float]],
        speed: float,
        is_danger: bool,
        permanent_flags: Dict[str, any]
    ):
        self.transcript = transcript
        self.location = location  # e.g., {"lat": 37.7749, "lon": -122.4194}
        self.location_history = location_history
        self.speed = speed
        self.is_danger = is_danger
        self.permanent_flags = permanent_flags  # e.g., {"home": {...}, "contacts": [...]}
