import re

CAMEL_CASE_PATTERN = re.compile(r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+")


def generate_unique_acronym(name: str, existing_prefixes: list[str]) -> str:
    """Generates a unique acronym for the given name by splitting it into
    words and creating an acronym."""
    words = _split_words(name)
    level = 1

    while True:
        acronym = _create_acronym(words, level)
        if acronym not in existing_prefixes:
            break
        level += 1

    return acronym + "_"


def _normalize(name: str) -> str:
    """Replaces common seperators from the given Name with a space."""
    return re.sub(r"[-_\s]+", " ", name.strip())


def _resolve_camel_case(name: str) -> list[str]:
    """Uses a Regular Expression, to seperate words that are chained together with camel case."""
    return CAMEL_CASE_PATTERN.findall(name)


def _split_words(name: str) -> list[str]:
    """Seperates the given name into its individual words by first normalizing it
    and then ressolving camel case."""
    normalized = _normalize(name=name)
    words = []

    for word in normalized.split():
        words.extend(_resolve_camel_case(word))

    return words


def _create_acronym(words: list[str], level: int = 1) -> str:
    """Creates an acronym from the given list of words by taking the first 'level'
    characters of each word. If a word is in uppercase and shorter than 4 characters,
    it is directly added to the acronym.
    """
    precise_name = []

    for word in words:
        if word.isupper() and len(word) < 4:
            precise_name.append(word)
        else:
            precise_name.append(word[:level].capitalize())
    return "".join(precise_name)
