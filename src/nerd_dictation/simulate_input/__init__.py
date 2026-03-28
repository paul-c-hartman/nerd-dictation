from typing import Callable

from nerd_dictation.simulate_input.xdotool import simulate_typing_with_xdotool
from nerd_dictation.simulate_input.ydotool import simulate_typing_with_ydotool
from nerd_dictation.simulate_input.dotool import simulate_typing_with_dotool, simulate_typing_with_dotoolc
from nerd_dictation.simulate_input.wtype import simulate_typing_with_wtype
from nerd_dictation.simulate_input.stdout import simulate_typing_with_stdout

input_fns: dict[str, Callable[[int, str], None]] = {
    "XDOTOOL": simulate_typing_with_xdotool,
    "YDOTOOL": simulate_typing_with_ydotool,
    "DOTOOL": simulate_typing_with_dotool,
    "DOTOOLC": simulate_typing_with_dotoolc,
    "WTYPE": simulate_typing_with_wtype,
    "STDOUT": simulate_typing_with_stdout,
}

__all__ = ["input_fns"]
