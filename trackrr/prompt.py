"""A simple prompt api to gather small bits of data like input function, as well as validate it for simple and cleaner code."""

from typing import Any, Callable, Optional

CustomValidator = Callable[
    [Any], bool
]  # A custom validator function that retunrs a boolean if certain requirements are met to the developers standards.


class Prompt:
    """Class that helps request input with a specific datatype"""

    def __init__(
        self,
        name: str = "",
        message: str = "",
        d_type: Any = str,
        custom_validator: Optional[CustomValidator] = None,
        transformer: Optional[Callable] = None,
    ):
        self.name = name
        self.message = message
        self.d_type = d_type
        self.custom_validator = custom_validator
        self.transfomer = transformer

    def prompt_user(self):
        answer = None

        while answer is None:
            answer = self.validate_answer(input(self.message + ": "))

            if (answer is not None) and self.transfomer:
                return self.transfomer(answer)

        return answer

    def validate_answer(self, answer: str) -> Optional[Any]:
        try:
            parsed_data = self.d_type(answer)
        except ValueError:
            print(f"\nThat isn't a valid {self.d_type.__name__}\n")
        else:
            if not self.custom_validator:
                return parsed_data

            elif self.custom_validator(parsed_data):
                return parsed_data


def get_multiple_input(input_params: tuple[Prompt]) -> dict:
    """Function able to get multiple input paramters from a user with data validation"""
    answers = {}

    for prompt in input_params:
        answers[prompt.name] = prompt.prompt_user()

    return answers
