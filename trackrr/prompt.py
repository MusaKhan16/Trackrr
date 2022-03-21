from typing import Any, Callable, Optional


class Prompt:
    """Class that helps request input with a specific datatype"""

    def __init__(
        self,
        name: str,
        message: str,
        d_type: Any = str,
        custom_validator: Optional[Callable] = None,
    ):
        self.name = name
        self.message = message
        self.d_type = d_type
        self.custom_validator = custom_validator

    def prompt_user(self):
        answer = None

        while answer is None:
            answer = self.validate_answer(input(self.message + ": "))
        return answer

    def validate_answer(self, answer: str) -> Optional[Any]:
        if isinstance(answer, self.d_type):
            return answer

        try:
            parsed_data = self.d_type(answer)
        except ValueError:
            print(f"That isn't a {self.d_type.__name__}")
        else:
            if not self.custom_validator:
                return parsed_data

            if self.custom_validator(parsed_data):
                return parsed_data


def get_multiple_input(input_params: tuple[Prompt]) -> dict:
    """Function able to get multiple input paramters from a user with data validation"""
    answers = {}

    for prompt in input_params:
        answers[prompt.name] = prompt.prompt_user()

    return answers
