from typing import Optional


def confirm_verification(answer: str) -> bool:
    """Converts a yes or no to a bool. Argument must be either yes or no"""
    return answer.lower() == "yes"


def is_yes_or_no(answer: str) -> bool:
    """Checks if a given input is either yes or no"""
    return answer.lower() in ("yes", "no")


def is_positive(num: int) -> Optional[bool]:
    """As per the name, checks if a number is positive and greater than 0"""
    return num > 0 or None
