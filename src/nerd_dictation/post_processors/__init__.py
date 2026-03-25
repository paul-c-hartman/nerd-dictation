from types import ModuleType
import sys
from typing import Any

post_processors = []

def register_post_processor(name: str, post_process_fn) -> None:
    post_processors.append((name, post_process_fn))

def load_post_processor(module_name: str) -> None:
    __import__(module_name)

def process_text(
    text: str,
    options: dict[str, dict[str, Any]] = {},
    # full_sentence: bool = False, # options['full_sentence']['enabled']: bool
    # numbers_as_digits: bool = False, # options['numbers']['as_digits']: bool
    # numbers_use_separator: bool = False, # options['numbers']['use_separator']: bool
    # numbers_min_value: Optional[int] = None, # options['numbers']['min_value']: Optional[int]
    # numbers_no_suffix: bool = False, # options['numbers']['no_suffix']: bool
) -> str:
    """
    Process the text with all registered post processors.
    """

    # Make absolutely sure we never add new lines in text that is typed in.
    # As this will press the return key when using automated key input.
    text = text.replace("\n", " ")
    words = text.split(" ")

    # Handle post processors that are registered by user configuration.
    for name, post_process_fn in post_processors:
        try:
            if options.get(name, {}).get("enabled", False):
                words = post_process_fn(words, options.get(name, {}))
        except Exception as ex:
            sys.stderr.write("Failed to run post processor %r with error %s\n" % (name, str(ex)))
            sys.exit(1)

    # Optional?
    if options.get("full_sentence", {}).get("enabled"):
        words[0] = words[0].capitalize()
        words[-1] = words[-1]

    return " ".join(words)


# Built-in post processors that are always available
load_post_processor("nerd_dictation.post_processors.full_sentence")
load_post_processor("nerd_dictation.post_processors.numbers")