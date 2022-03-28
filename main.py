from turtle import distance
import trackrr as tr
import validators
import utils

from dataclasses import asdict
from rich.console import Console
from copy import deepcopy


# Make sure degrees dont go over or below 360


def main():

    descision_mapping = {
        "c": prompt_trail_creation,
        "r": prompt_review_track,
    }

    user_descision = ""

    console.rule(
        "[bold dodger_blue2]Welcome! Trackrr is a simple open source software that allows one to track and manage their mountain bike parks[/bold dodger_blue2]"
    )
    console.print("You can add trails to the database OR review old ones to be updated")

    while user_descision != "l":
        user_descision = input(
            "\n[L] Leave || [C] Create new Track || [R] Review track from database: "
        ).lower()

        if user_descision != "L" and user_descision in descision_mapping:
            descision_mapping.get(user_descision)()

    console.print("[bold]Bye then![/bold] :wave:")


def prompt_review_track():
    """A Prompt for reviewing and editing tracks"""

    console.print("Attempting to Load tracks from database...")

    sub_prompt_decision_mapping = {
        "a": print_paths_under_construction,
        "b": prompt_metric_conversion,
        "d": prompt_trail_deletion,
        "sd": prompt_deletion_of_sections,
        "sc": prompt_creation_of_sections,
    }

    tracks = database.all()

    if not tracks:
        print("Whoops! You havent created any tracks...\n")
        return

    tracks = [tr.Trail(**track) for track in tracks]
    console.print("\n[green]Loaded tracks![/green] :white_check_mark:")

    for idx, trail in enumerate(tracks):
        console.print(f"[bold]{idx + 1}.[/bold]", trail.padded_repr())

    user_index_choice = (
        tr.Prompt(
            name="user_trail_index",
            message="Which Trail do you want to check? Pass an index",
            d_type=int,
            custom_validator=(lambda num: len(tracks) >= num > 0 or None),
        ).prompt_user()
        - 1
    )

    user_trail_choice = tracks[user_index_choice]

    user_decision_choice = ""

    while user_decision_choice.lower() != "l":
        console.print(user_trail_choice)

        user_decision_choice = (
            tr.Prompt(
                message="""\nWhat do you want to do with the Trail? type nothing to leave\n\t[a](Retrieve Sections under Construction)\n\t[b](Perform metric conversions on the numbers distance, elevation, angle)\n\t[sd](Delete a section)\n\t[sc](Add Section)\n\t[d](Delete the trail)\n[L](Leave)""",
                custom_validator=(
                    lambda user_decision: user_decision.lower()
                    in sub_prompt_decision_mapping.keys()
                    or user_decision.lower() == "l"
                ),
            )
            .prompt_user()
            .lower()
        )

        if user_decision_choice.lower() == "l":
            return

        if user_decision_choice.lower() == "d":
            sub_prompt_decision_mapping.get("d")(user_trail_choice)
            break  # Justifiable use for break, this case is a wildcard and would be better of taken care with a simple keyword.

        sub_prompt_decision_mapping.get(user_decision_choice)(user_trail_choice)


def prompt_trail_creation():
    """Prompts a series of question to create a track"""

    user_created_trail = tr.get_multiple_input(
        (
            tr.Prompt(name="name", message="Enter the name of the track"),
            tr.Prompt(name="description", message="Enter the description of the track"),
            tr.Prompt(
                name="difficulty",
                message="Enter the difficulty of the track by standard [Very Easy, Easy, Difficult, Very Difficult, Very Very Difficult](Case Sensitive)",
                d_type=tr.TrackDifficulty,
            ),
            tr.Prompt(
                name="elevation",
                message="Enter the elevation of the track in meters",
                d_type=int,
                custom_validator=validators.is_positive,
            ),
        )
    )

    current_trail = tr.Trail(**user_created_trail)

    console.print("\nSuccessfully created Trail object:\n", current_trail.padded_repr())

    user_path_choice = input(
        "\nDo you possibly want to add any sections to the track Yes [Y default] No [N]: "
    ).lower()

    while user_path_choice != "n":
        user_created_path = tr.get_multiple_input(
            (
                tr.Prompt(
                    name="angle_slant",
                    message="Enter the slant of the section in degrees",
                    d_type=int,
                    custom_validator=validators.is_positive,
                ),
                tr.Prompt(
                    name="distance",
                    message="State the total distance of the section in meters",
                    d_type=int,
                    custom_validator=validators.is_positive,
                ),
                tr.Prompt(
                    name="terrain_type",
                    message="State the type of terrain [Rocky, Smooth, Gravel, Muddy, Snowy](Case Sensitive)",
                    d_type=tr.TerrainType,
                ),
                tr.Prompt(
                    name="under_construction",
                    message="Is this section under construction? True ortype nothing if false",
                    d_type=bool,
                ),
            )
        )

        user_created_path_object = tr.Path(**user_created_path)

        user_choice = input(
            f"\nDo you want to add this section to the Track? default is [Y] Yes [N] no {user_created_path_object}"
        )

        if user_choice.lower() != "n":
            current_trail.add_section(user_created_path_object)

        user_path_choice = input(
            "Do you want to add another section default is [Y] Yes or type [N] for no: "
        ).lower()

    try:
        database.insert_item(asdict(current_trail))
    except tr.NotUnique:
        console.print(
            "[bold red]Whoops! That name already exists in the database, please try again :no_entry:[/bold red]"
        )
    else:
        console.print(
            "[green bold]\nSession finished, added\n[/green bold]", str(current_trail)
        )


def print_paths_under_construction(trail: tr.Trail):
    if not trail.under_construction:
        console.print(
            "[red bold]Oh! there are no paths under construction for this trail[/red bold]"
        )
    else:
        for path in trail.get_paths_under_construction():
            console.print(str(path))


def prompt_metric_conversion(trail: tr.Trail):
    """Prompts a sequence of questions on metric conversion"""

    distance_metric = tr.Prompt(
        message=(
            """
                Enter the new units you want to convert distance currently [m]
                Options: 
                    Distance 📏:
                        [KM]:  Kilometers
                        [MM]: Milimeters
                        [CM]: Centimeters
                        [MI]: Miles
                """
        ),
        custom_validator=(lambda answer: answer.lower() in ["mm", "cm", "km", "mi"]),
        transformer=str.lower,
    ).prompt_user()

    user_wants_radians = tr.Prompt(
        message="Do you want to convert degrees to radians?",
        custom_validator=(lambda answer: answer.lower() in ("yes", "no")),
        transformer=validators.confirm_verification,
    ).prompt_user()

    new_trail_elevation = trail.elevation * utils.convert_metric_distance(
        distance_metric
    )

    console.print(f"\nTrail Elevation {new_trail_elevation}{distance_metric}")

    for idx, path in enumerate(deepcopy(trail.sections)):
        path.update_distance(utils.convert_metric_distance(distance_metric))

        if user_wants_radians:
            path.angle_slant = utils.convert_to_radians(path.angle_slant)

        console.print(
            f"\nPath {idx + 1}.) {path.distance=}{distance_metric} {path.angle_slant=}{'rad' if user_wants_radians else 'deg'}\n"
        )


def prompt_trail_deletion(trail: tr.Trail):
    """A series of prompts that will allow a user to delete a trail"""

    user_verification = tr.Prompt(
        message="Are you sure you want to delete this",
        custom_validator=(lambda answer: answer.lower() in ("yes", "no")),
        transformer=validators.confirm_verification,
    ).prompt_user()

    if not user_verification:
        console.print("[cyan bold]OK object not deleted[/cyan bold]")
        return

    database.delete_item(asdict(trail))
    console.print(
        f"[green bold]Successfully deleted [underline]{trail.name}[/underline][/green bold]"
    )


def prompt_creation_of_sections(trail: tr.Trail):
    """Prompt that allows user to add sections to a trail"""
    user_new_path = tr.get_multiple_input(
        (
            tr.Prompt(
                name="angle_slant",
                message="Enter the slant of the section in degrees",
                d_type=int,
                custom_validator=(lambda angle: -360 <= angle <= 360),
            ),
            tr.Prompt(
                name="distance",
                message="State the total distance of the section in meters",
                d_type=int,
                custom_validator=validators.is_positive,
            ),
            tr.Prompt(
                name="terrain_type",
                message="State the type of terrain [Rocky, Smooth, Gravel, Muddy, Snowy](Case Sensitive)",
                d_type=tr.TerrainType,
            ),
            tr.Prompt(
                name="under_construction",
                message="Is this section under construction? type nothing if false",
                d_type=bool,
            ),
        )
    )

    new_user_created_path = tr.Path(**user_new_path)

    console.print(new_user_created_path.padded_repr())

    user_verification = validators.confirm_verification(
        tr.Prompt(
            message=f"Are you sure you want to create this path [Yes, No]?",
            custom_validator=(lambda answer: answer.lower() in ("yes", "no")),
        ).prompt_user()
    )

    if not user_verification:
        console.print("[blue bold]Ok didnt make new path 👌")
        return

    trail.add_section(new_user_created_path)
    database.update(asdict(trail))

    console.print("[green bold]Successfully added new path to trail ✅[/green bold]")


def prompt_deletion_of_sections(trail: tr.Trail):
    if not trail.sections:
        console.print("[bold red]This trail doesnt have sections![/bold red]")
        return

    for idx, section in enumerate(trail.sections):
        console.print(f"{idx + 1}.)", section.padded_repr())

    user_index_choice = (
        tr.Prompt(
            message="Which Trail do you want to check? Pass an index",
            d_type=int,
            custom_validator=(lambda num: len(trail.sections) >= num > 0 or None),
        ).prompt_user()
        - 1
    )

    user_verification = validators.confirm_verification(
        tr.Prompt(
            message=f"Are you sure you want to delete this {trail.sections[user_index_choice]} [Yes, No]",
            custom_validator=(lambda answer: answer.lower() in ("yes", "no")),
        ).prompt_user()
    )

    if not user_verification:
        console.print(f"[blue bold]Ok didnt delete item[/blue bold]")
        return

    trail.remove_section(user_index_choice)
    database.update(asdict(trail))

    console.print("[bold green]Successfully updated item![/bold green]")


if __name__ == "__main__":
    """Config variables for global usage"""
    database = tr.TrackDatabase("./MTB.json", indent=4)
    console = Console()

    main()
