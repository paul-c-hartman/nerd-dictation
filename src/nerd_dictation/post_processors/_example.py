"""
This file implements an example post-processor that capitalizes every word in the text.
It's meant to be used solely as an example of how to implement a post-processor.
"""

from nerd_dictation.post_processors import register_post_processor
from typing import Any

def capitalize_all_words(words: list[str], options: dict[str, Any] = {}) -> list[str]:
    for i in range(len(words)):
        words[i] = words[i].capitalize()
    return words

register_post_processor("_example", capitalize_all_words)