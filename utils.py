import enum
import sys

class Color(enum.Enum):
    RED = "\033[1;31m"  
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"


def pretty_print(message: str, color:str, *args, **kwargs) -> None:
    sys.stdout.write(color)
    print('-'*len(message))
    print(message)
    print('-'*len(message))
    sys.stdout.write(Color.RESET.value)


def error_print(message: str) -> None:
    pretty_print(message, Color.RED.value)


def success_print(message: str) -> None:
    pretty_print(message, Color.GREEN.value)
