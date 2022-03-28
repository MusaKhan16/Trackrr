from typing import Optional


def confirm_verification(answer: str) -> bool:
    """Converts a yes or no to a bool. Argument must be either yes or no"""
    return answer.lower() == "yes"


def is_positive(num: int) -> Optional[bool]:
    return num >= 0 or None
