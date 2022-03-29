import trackrr as tr
import quick_prompts
import utils


from dataclasses import asdict
from rich.console import Console
from copy import deepcopy


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
        "v": console.print,
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
            message="\nWhich Trail do you want to check? Pass an index",
            d_type=int,
            custom_validator=(lambda num: len(tracks) >= num > 0 or None),
        ).prompt_user()
        - 1
    )

    user_trail_choice = tracks[user_index_choice]

    user_decision_choice = ""

    while user_decision_choice.lower() != "l":

        user_decision_choice = tr.Prompt(
            message="""\nWhat do you want to do with the Trail? type nothing to leave\n\t[v](View current Trail)\n\t[a](Retrieve Sections under Construction)\n\t[b](Perform metric conversions on the numbers distance, elevation, angle)\n\t[sd](Delete a section)\n\t[sc](Add Section)\n\t[d](Delete the trail)\n[L](Leave)""",
            custom_validator=(
                lambda user_decision: user_decision.lower()
                in sub_prompt_decision_mapping.keys()
                or user_decision.lower() == "l"
            ),
            transformer=str.lower,
        ).prompt_user()

        if user_decision_choice.lower() == "l":
            return

        if user_decision_choice.lower() == "d":
            sub_prompt_decision_mapping.get("d")(user_trail_choice)
            break  # Justifiable use for break, this case is a wildcard and would be better of taken care with a simple keyword.

        sub_prompt_decision_mapping.get(user_decision_choice)(user_trail_choice)


def prompt_trail_creation():
    """Prompts a series of question to create a track"""

    user_created_trail = tr.get_multiple_input(quick_prompts.CREATE_TRAIL)

    current_trail = tr.Trail(**user_created_trail)

    console.print("\nSuccessfully created Trail object:\n", current_trail.padded_repr())

    user_path_choice = quick_prompts.ConfirmationPrompt(
        "\nDo you possibly want to add any sections to the track", transformer=str.lower
    ).prompt_user()

    while user_path_choice != "no":
        user_created_path = tr.get_multiple_input(quick_prompts.CREATE_PATH)

        user_created_path_object = tr.Path(**user_created_path)

        user_choice = quick_prompts.ConfirmationPrompt(
            f"Are you sure you want to add this section to the Track"
        ).prompt_user()

        if user_choice:
            current_trail.add_section(user_created_path_object)

        user_path_choice = quick_prompts.ConfirmationPrompt(
            "Do you want to add another section",
            transformer=str.lower,
        ).prompt_user()

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

    user_wants_radians = quick_prompts.ConfirmationPrompt(
        message="Do you want to convert degrees to radians"
    ).prompt_user()

    new_trail_elevation = trail.elevation * utils.convert_metric_distance(
        distance_metric
    )

    metric_conversion_number = utils.convert_metric_distance(distance_metric)

    for idx, path in enumerate(deepcopy(trail.sections)):
        path.update_distance(metric_conversion_number)

        if user_wants_radians:
            path.angle_slant = utils.convert_to_radians(path.angle_slant)

        console.print(
            f"\nPath {idx + 1}.) {path.distance=}{distance_metric} {path.angle_slant=}{'rad' if user_wants_radians else 'deg'}\n"
        )

    console.print(f"\nTrail Elevation {new_trail_elevation}{distance_metric}")
    console.print(
        f"\nNew total distance = {trail.total_distance * metric_conversion_number}{distance_metric}"
    )


def prompt_trail_deletion(trail: tr.Trail):
    """A series of prompts that will allow a user to delete a trail"""

    user_verification = quick_prompts.ConfirmationPrompt(
        "Are you sure you want to delete this",
    ).prompt_user()

    if not user_verification:
        console.print("\n[cyan bold]OK object not deleted[/cyan bold]")
        return

    database.delete_item(asdict(trail))
    console.print(
        f"\n[green bold]Successfully deleted [underline]{trail.name}[/underline][/green bold]"
    )


def prompt_creation_of_sections(trail: tr.Trail):
    """Prompt that allows user to add sections to a trail"""
    user_new_path = tr.get_multiple_input(quick_prompts.CREATE_PATH)

    new_user_created_path = tr.Path(**user_new_path)

    console.print(new_user_created_path.padded_repr())

    user_verification = quick_prompts.ConfirmationPrompt(
        "\nAre you sure you want to create this path",
    ).prompt_user()

    if not user_verification:
        console.print("\n[blue bold]Ok didnt make new path 👌")
        return

    trail.add_section(new_user_created_path)
    database.update_item(asdict(trail))

    console.print("[green bold]Successfully added new path to trail ✅[/green bold]")


def prompt_deletion_of_sections(trail: tr.Trail):
    if not trail.sections:
        console.print("[bold red]This trail doesnt have sections![/bold red]")
        return

    for idx, section in enumerate(trail.sections):
        console.print(f"{idx + 1}.)", section.padded_repr())

    user_index_choice = (
        tr.Prompt(
            message="\nWhich Trail do you want to check? Pass an index",
            d_type=int,
            custom_validator=(lambda num: len(trail.sections) >= num > 0 or None),
        ).prompt_user()
        - 1
    )

    user_verification = quick_prompts.ConfirmationPrompt(
        message=f"Are you sure you want to delete that section",
    ).prompt_user()

    if not user_verification:
        console.print(f"\n[blue bold]Ok didnt delete item 👌[/blue bold]")
        return

    trail.remove_section(user_index_choice)
    database.update_item(asdict(trail))

    console.print("[bold green]Successfully updated item![/bold green]")


if __name__ == "__main__":
    """Config variables for global usage"""
    database = tr.TrackDatabase("./MTB.json", indent=4)
    console = Console()

    main()
