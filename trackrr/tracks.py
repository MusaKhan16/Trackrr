from typing import List
from dataclasses import dataclass, field
from trackrr.enums import TerrainType, TrackDifficulties


@dataclass
class Path:
    """
    Path class to be stored in Trail class as a section/part of a trail
    """

    distance: int
    angle_slant: int
    terrain_type: TerrainType

    def __str__(self):
        """Representation of a section of a trail/path"""

        return (
            f"\nDistance: {self.distance} meters at an angle of {self.angle_slant}°\n"
            f"Type of terrain {self.terrain_type}"
        )


@dataclass
class Trail:
    """Trail Class To initialize a mountain bike Track"""

    elevation: int
    difficulty: TrackDifficulties
    sections: List[Path] = field(default_factory=list)
    under_contruction: bool = False

    @property
    def total_distance(self):
        """Get sum of all sections"""
        return sum(map(lambda path: path.distance, self.sections))

    def describe_sections(self):
        """Describe sections by printing each path within the array"""
        for path in self.sections:
            print(path)

    def __str__(self):
        """A string representation of the Trail Object"""

        return (
            f"\nDifficulty: {self.difficulty}\n"
            f"Elevation above ground: {self.elevation} meters\n"
            f"Amount of sections: {len(self.sections)}\n"
            f"Total distance: {self.total_distance} meters\n"
            f"Under Construction: {self.under_contruction}"
        )
