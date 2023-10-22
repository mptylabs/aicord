import pytest
from aicord.utils.string import split_paragraph_chunks

def test_split_paragraph_chunks():
    test_cases = [
        ("Hello, world!\n\nThis is a test.", 10, ["Hello, world!", "This is a", "test."]),
        ("", 10, []),
        ("No paragraphs here", 10, ["No", "paragraphs", "here"]),
        ("This paragraph is too long for the limit", 10, ["This", "paragraph", "is too", "long for", "the limit"]),
    ]

    for text, max_length, expected in test_cases:
        result = split_paragraph_chunks(text, max_length)
        assert result == expected
