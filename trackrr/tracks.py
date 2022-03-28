from typing import List
from dataclasses import dataclass, field
from trackrr.enums import TerrainType, TrackDifficulty
from rich.padding import Padding


@dataclass
class Path:
    """
    Path class to be stored in Trail class as a section/part of a trail
    """

    distance: int
    angle_slant: int
    terrain_type: TerrainType
    under_construction: bool = False

    def __post_init__(self):
        """Post init used to validate data"""
        if not isinstance(self.terrain_type, TerrainType):
            self.terrain_type = TerrainType(self.terrain_type)

    def padded_repr(self):
        return Padding(str(self), (0, 4))

    def update_distance(self, new_distance: int | float):
        """Updates distance to new converted metric"""
        self.distance *= new_distance

    def update_angle_slant(self, new_angle_slant: int | float):
        """Updates the angle to new converted metric"""
        self.angle_slant *= new_angle_slant

    def __str__(self):
        """Representation of a section of a trail/path"""

        return (
            f"\nDistance: {self.distance} meters at an angle of {self.angle_slant}°\n"
            f"Type of terrain {self.terrain_type}\n"
        )


@dataclass
class Trail:
    """
    Trail Class To initialize a mountain bike Track
    """

    name: str
    description: str
    elevation: int
    difficulty: TrackDifficulty
    sections: List[Path] = field(default_factory=list)

    def __post_init__(self):
        """Post init used to validate data"""
        if self.sections:
            if isinstance(self.sections[0], Path):
                return

            self.sections = [Path(**section) for section in self.sections]

        if not isinstance(self.difficulty, TrackDifficulty):
            self.difficulty = TrackDifficulty(self.difficulty)

    @property
    def total_distance(self):
        """Get sum of all sections"""
        return sum(path.distance for path in self.sections)

    @property
    def under_construction(self):
        """Return a boolean depending on whether any section is under construction"""
        return any(path.under_construction for path in self.sections)

    def get_paths_under_construction(self) -> List[Path]:
        """Retriving those paths of which are under construction"""
        return [path for path in self.sections if path.under_construction]

    def add_section(self, path: Path):
        """Appends a path to the sections array"""
        self.sections.append(path)

    def remove_section(self, index: int):
        """Removes a section from the sections array depending on a given index"""
        self.sections.pop(index)

    def padded_repr(self):
        return Padding(str(self), (0, 4))

    def update_metrics(
        self,
    ):
        """Updates the metrics of the trail"""

    def __str__(self):
        """A string representation of the Trail Object"""

        return (
            f"---------------{self.name}----------------\n"
            f"Difficulty: {self.difficulty}\n"
            f"Elevation above ground: {self.elevation} meters\n"
            f"Amount of sections: {len(self.sections)}\n"
            f"Total distance: {self.total_distance} meters\n"
            f"Under Construction: {self.under_construction}\n\n"
            f"{self.description}\n{'_'*50}\n"
            f"Sections:"
            + ("\n\t".join(map(str, self.sections)) if self.sections else "\n\tNone")
        )
