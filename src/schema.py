from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class LocationPoint:
    timestamp: str
    lat: float
    lon: float

@dataclass
class DangerFlags:
    tone_anxiety: bool
    danger_keywords: bool
    unusual_location: bool
    fast_movement: bool
    silent_mode: Optional[bool] = False  # optional, can be set by planner

@dataclass
class InputData:
    voice_transcript: str
    location_history: List[LocationPoint]
    danger_flags: DangerFlags
    speed_mph: float
    speed_change: float
    voice_output_disabled: bool
    timestamp: str

