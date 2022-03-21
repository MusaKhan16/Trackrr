from enum import Enum


class TrackDifficulty(str, Enum):
    WHITE_CIRCLE = "Very Easy"
    GREEN_CIRCLE = "Easy"
    BLUE_SQUARE = "Difficult"
    BLACK_DIAMOND = "Very Difficult"
    DOUBLE_BLACK_DIAMOND = "Very Very Difficult"


class TerrainType(str, Enum):
    ROCKY = "Rocky"
    SMOOTH = "Smooth"
    GRAVEL = "Gravel"
    MUDDY = "Muddy"
