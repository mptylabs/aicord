import unittest
from aicord.utils.string import split_paragraph_chunks

class TestSplitParagraphChunks(unittest.TestCase):
    def setUp(self):
        self.short_text = "This is a short text."
        self.exact_text = "This is an exact text." * 100
        self.long_text = "This is a long text." * 200
        self.empty_text = ""
        self.no_space_text = "ThisTextHasNoSpaces."

    def test_short_text(self):
        result = split_paragraph_chunks(self.short_text, 2000)
        self.assertEqual(result, [self.short_text])

    def test_exact_text(self):
        result = split_paragraph_chunks(self.exact_text, 2000)
        self.assertEqual(result, [self.exact_text[i:i+2000] for i in range(0, len(self.exact_text), 2000)])

    def test_long_text(self):
        result = split_paragraph_chunks(self.long_text, 2000)
        self.assertEqual(result, [self.long_text[i:i+2000] for i in range(0, len(self.long_text), 2000)])

    def test_empty_text(self):
        result = split_paragraph_chunks(self.empty_text, 2000)
        self.assertEqual(result, [])

    def test_no_space_text(self):
        result = split_paragraph_chunks(self.no_space_text, 2000)
        self.assertEqual(result, [self.no_space_text])

if __name__ == '__main__':
    unittest.main()
