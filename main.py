import trackrr as tr
from typing import Optional, NotImplemented
from dataclasses import asdict
from rich.console import Console


def main():

    descision_mapping = {
        "c": prompt_track,
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
    console.print("Attempting to Load tracks from database...")

    descision_mapping = {"a": print_paths_under_construction}

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

    console.print(user_trail_choice)

    user_desicion_choice = input(
        "What do you want to do with the Trail [a](Retrieve Sections under Construction): "
    )

    descision_mapping.get(user_desicion_choice)(user_trail_choice)


def prompt_track():
    user_created_trail = tr.get_multiple_input(
        (
            tr.Prompt(name="name", message="Enter the name of the track"),
            tr.Prompt(name="description", message="Enter the description of the track"),
            tr.Prompt(
                name="difficulty",
                message="Enter the difficulty of the track by standard",
                d_type=tr.TrackDifficulty,
            ),
            tr.Prompt(
                name="elevation",
                message="Enter the elevation of the track in meters",
                d_type=int,
                custom_validator=validate_numbers,
            ),
        )
    )

    current_trail = tr.Trail(**user_created_trail)

    print("\nSuccessfully created Trail object:\n", current_trail)

    user_path_choice = input(
        "\nDo you possibly want to add any sections to the track Yes [Y] No [N]: "
    )

    while user_path_choice != "N":
        user_created_path = tr.get_multiple_input(
            (
                tr.Prompt(
                    name="angle_slant",
                    message="Enter the slant of the section",
                    d_type=int,
                    custom_validator=validate_numbers,
                ),
                tr.Prompt(
                    name="distance",
                    message="State the total distance of the section",
                    d_type=int,
                    custom_validator=validate_numbers,
                ),
                tr.Prompt(
                    name="terrain_type",
                    message="State the type of terrain",
                    d_type=tr.TerrainType,
                ),
                tr.Prompt(
                    name="under_construction",
                    message="Is this section under construction? type nothing if false",
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
            "Do you want to add another track? default is [Y] Yes or type [N] for no: "
        )

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


def validate_numbers(num: int) -> Optional[bool]:
    return num >= 0 or None


def print_paths_under_construction(trail: tr.Trail):
    for path in trail.get_paths_under_construction():
        console.print(path)


def prompt_metric_conversion(trail: tr.Trail):
    """To be implemented"""
    ...


if __name__ == "__main__":
    """Config variables for global usage"""
    database = tr.TrackDatabase("./MTB.json", indent=4)
    console = Console()

    main()
