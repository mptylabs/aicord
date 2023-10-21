import unittest

from aicord.utils.string import split_paragraph_chunks


class TestSplitParagraphChunks(unittest.TestCase):
    def test_short_text(self):
        """
        Test case where the text is shorter than the maximum length.
        """
        text = "This is a short paragraph."
        max_length = 100
        expected_output = ["This is a short paragraph."]
        self.assertEqual(split_paragraph_chunks(text, max_length), expected_output)

    def test_exact_length_text(self):
        """
        Test case where the text is exactly the maximum length.
        """
        text = "a" * 100
        max_length = 100
        expected_output = ["a" * 100]
        self.assertEqual(split_paragraph_chunks(text, max_length), expected_output)

    def test_long_text(self):
        """
        Test case where the text is longer than the maximum length.
        """
        text = "a" * 200
        max_length = 100
        expected_output = ["a" * 100, "a" * 100]
        self.assertEqual(split_paragraph_chunks(text, max_length), expected_output)

    def test_multiple_paragraphs(self):
        """
        Test case where the text contains multiple paragraphs.
        """
        text = "This is the first paragraph.\n\nThis is the second paragraph."
        max_length = 100
        expected_output = [
            "This is the first paragraph.",
            "This is the second paragraph.",
        ]
        self.assertEqual(split_paragraph_chunks(text, max_length), expected_output)
    
    def test_multiple_small_paragraphs(self):
        """
        Test case where multiple paragraphs are smaller than max length, so that 2 paragraphs fit into 1 chunk, but 3rd one doesn't.
        """
        text = "This is the first paragraph. " + "This is the second paragraph.\n\n" + "This is the third paragraph."
        max_length = 100
        expected_output = [
            "This is the first paragraph. This is the second paragraph.",
            "This is the third paragraph.",
        ]
        self.assertEqual(split_paragraph_chunks(text, max_length), expected_output)


if __name__ == "__main__":
    unittest.main()
