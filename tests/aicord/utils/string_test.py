import unittest
from aicord.utils.string import split_paragraph_chunks

class TestSplitParagraphChunks(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            ("Hello, world!\n\nThis is a test.", 10, ["Hello, world!", "This is a", "test."]),
            ("First paragraph.\n\nSecond paragraph.\n\nThird paragraph is too long.", 20, ["First paragraph.", "Second paragraph.", "Third", "paragraph is", "too long."]),
        ]

    def test_case_1(self):
        text, max_length, expected = self.test_cases[0]
        result = split_paragraph_chunks(text, max_length)
        self.assertEqual(result, expected)

    def test_split_paragraph_chunks(self):
        text, max_length, expected = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph is too long.", 20, ["First paragraph.", "Second paragraph.", "Third", "paragraph is", "too long."]
        result = split_paragraph_chunks(text, max_length)
        self.assertEqual(result, expected)
