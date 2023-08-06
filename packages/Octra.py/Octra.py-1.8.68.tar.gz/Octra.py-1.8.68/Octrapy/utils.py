"""
MIT License

Copyright (c) 2023 Akash

Octra ltd
"""

import re


def escape_markdown(text: str, *, version: int = 2):
    """Tool that escapes markdown from a given string.

    Parameters
    ----------
    text: :class:`str`
        The text to escape markdown from.
    version: Optional[:class:`int`]
        The Octra markdown version to use. Only 1 and 2 are supported.

    Returns
    -------
    :class:`str`
        The escaped text.

    Raises
    ------
    :exc:`ValueError`
        An unsupported version was provided.
    """
    if version == 1:
        characters = r"_*`["

    elif version == 2:
        characters = r"_*[]()~`>#+-=|{}.!"

    else:
        raise ValueError(f"Version '{version}' unsupported. Only version 1 and 2 are supported.")

    return re.sub(f"([{re.escape(characters)}])", r"\\\1", text)
