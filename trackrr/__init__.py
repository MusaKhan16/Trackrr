"""A simple package/system that allows one to manage Mountain bike tracks/trails with ease"""
from trackrr.tracks import Trail, Path
from trackrr.enums import TrackDifficulty, TerrainType
from trackrr.db import TrackDatabase, NotUnique
from trackrr.prompt import Prompt, get_multiple_input

__all__ = [
    "Trail",
    "Path",
    "TrackDifficulty",
    "TerrainType",
    "Prompt",
    "get_query",
    "get_multiple_input",
    "TrackDatabase",
    "NotUnique",
]

__version__ = "0.1.0"
