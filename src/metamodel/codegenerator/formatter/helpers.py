import re


def _to_words(name: str) -> list[str]:
    """
    Splits any identifier style into a list of lowercase words.
    Handles snake_case, PascalCase, camelCase, UPPER_SNAKE_CASE, and mixed forms.

    Examples:
        "test_name"  → ["test", "name"]
        "TestName"   → ["test", "name"]
        "testName"   → ["test", "name"]
        "TEST_NAME"  → ["test", "name"]
        "HTMLParser" → ["html", "parser"]
    """
    # camelCase / PascalCase: insert a space before an uppercase that follows a lowercase/digit
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    # Acronym runs: "HTMLParser" → "HTML Parser"
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    # Treat underscores as word boundaries
    s = s.replace('_', ' ')
    return [w.lower() for w in s.split() if w]


def to_pascal_case(name: str) -> str:
    """test_name / testName / TestName  →  TestName"""
    return ''.join(word.capitalize() for word in _to_words(name))


def to_snake_case(name: str) -> str:
    """test_name / testName / TestName  →  test_name"""
    return '_'.join(_to_words(name))


def to_upper_snake_case(name: str) -> str:
    """test_name / testName / TestName  →  TEST_NAME"""
    return '_'.join(word.upper() for word in _to_words(name))


def to_camel_case(name: str) -> str:
    """test_name / TestName / TestName  →  testName"""
    words = _to_words(name)
    return words[0] + ''.join(word.capitalize() for word in words[1:]) if words else ''
