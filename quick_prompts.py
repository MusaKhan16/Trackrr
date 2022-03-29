import validators
from typing import Callable
from trackrr import Prompt, TerrainType, TrackDifficulty


class ConfirmationPrompt(Prompt):
    """
    Subclass of the generic Prompt class to provide an implementation for a specific type of question.
    Essentially can be added in templates like CREATE_PATH as it inherits from the main class.
    When the get multiple prompt function is run it will be able to call this with the same prompt_user()
    method.
    """

    def __init__(
        self, message: str, transformer: Callable = validators.confirm_verification
    ):
        super().__init__(
            name="under_construction",
            message=(message + " [Yes, No]"),
            custom_validator=validators.is_yes_or_no,
            transformer=transformer,
        )


# Template prompt sequences of creating a path and trail objects.
# All prompts have data validation with cleaner and simpler looking code.

CREATE_PATH = (
    Prompt(
        name="angle_slant",
        message="Enter the slant of the section in degrees",
        d_type=int,
        custom_validator=(
            lambda angle: -360 <= angle <= 360
        ),  # Essentially the use of the and keyword since under the hood python chains the following code to -360 <= angle and angle <= 360. Simply syntactical sugar.
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
    ConfirmationPrompt(
        message="Is this section under construction",
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
