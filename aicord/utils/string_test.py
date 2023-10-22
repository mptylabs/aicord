import pytest
from aicord.utils.string import split_paragraph_chunks

def test_split_paragraph_chunks():
    test_cases = [
        ("", 10, [""]),
        ("Hello, world!", 10, ["Hello,", "world!"]),
        ("Hello, world!\n\nHow are you?", 10, ["Hello,", "world!", "How are", "you?"]),
        ("Hello, world!\n\nHow are you?", 20, ["Hello, world!", "How are you?"]),
        ("This is a long paragraph that needs to be split into multiple chunks because it exceeds the maximum length.", 20, ["This is a long", "paragraph that needs", "to be split into", "multiple chunks", "because it exceeds", "the maximum length."]),
        ("This is a single paragraph.", 50, ["This is a single paragraph."]),
        ("This is a single paragraph that exceeds the maximum length.", 10, ["This is a", "single", "paragraph", "that", "exceeds the", "maximum", "length."])
    ]

    for text, max_length, expected in test_cases:
        result = split_paragraph_chunks(text, max_length)
        unittest.TestCase().assertEqual(result, expected)
