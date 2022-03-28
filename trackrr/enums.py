from enum import Enum


class TrackDifficulty(str, Enum):
    """Difficulties of a track constants relative to industry standards"""

    WHITE_CIRCLE = "Very Easy"
    GREEN_CIRCLE = "Easy"
    BLUE_SQUARE = "Difficult"
    BLACK_DIAMOND = "Very Difficult"
    DOUBLE_BLACK_DIAMOND = "Very Very Difficult"


class TerrainType(str, Enum):
    """Types of terrain types"""

    ROCKY = "Rocky"
    SMOOTH = "Smooth"
    GRAVEL = "Gravel"
    MUDDY = "Muddy"
    SNOWY = "Snowy"
