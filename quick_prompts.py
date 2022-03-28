import validators
from trackrr import Prompt, TerrainType, TrackDifficulty

CREATE_PATH = (
    Prompt(
        name="angle_slant",
        message="Enter the slant of the section in degrees",
        d_type=int,
        custom_validator=(lambda angle: -360 <= angle <= 360),
    ),
    Prompt(
        name="distance",
        message="State the total distance of the section in meters",
        d_type=int,
        custom_validator=validators.is_positive,
    ),
    Prompt(
        name="terrain_type",
        message="State the type of terrain [Rocky, Smooth, Gravel, Muddy, Snowy](Case Sensitive)",
        d_type=TerrainType,
    ),
    Prompt(
        name="under_construction",
        message="Is this section under construction? type nothing if false",
        d_type=bool,
    ),
)

CREATE_TRAIL = (
    Prompt(name="name", message="Enter the name of the track"),
    Prompt(name="description", message="Enter the description of the track"),
    Prompt(
        name="difficulty",
        message="Enter the difficulty of the track by standard [Very Easy, Easy, Difficult, Very Difficult, Very Very Difficult](Case Sensitive)",
        d_type=TrackDifficulty,
    ),
    Prompt(
        name="elevation",
        message="Enter the elevation of the track in meters",
        d_type=int,
        custom_validator=validators.is_positive,
    ),
)

YES_OR_NO = Prompt(custom_validator=(lambda answer: answer.lower() in ("yes", "no")))
