from nerd_dictation.post_processors import register_post_processor
from typing import Any

def full_sentence(words: list[str], options: dict[str, Any] = {}) -> list[str]:
    words[0] = words[0].capitalize()
    words[-1] = words[-1]
    return words

register_post_processor("full_sentence", full_sentence)