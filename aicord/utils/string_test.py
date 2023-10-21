import unittest

from aicord.utils.string import split_paragraph_chunks


class TestSplitParagraphChunks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(split_paragraph_chunks("", 1000), [])

    def test_no_paragraphs(self):
        self.assertEqual(
            split_paragraph_chunks("Hello, world!", 1000), ["Hello, world!"]
        )

    def test_one_long_paragraph(self):
        long_paragraph = "A" * 2000
        self.assertEqual(
            split_paragraph_chunks(long_paragraph, 1000), ["A" * 1000, "A" * 1000]
        )

    def test_many_short_paragraphs(self):
        paragraphs = ["Hello, world!"] * 100
        self.assertEqual(
            split_paragraph_chunks("\n\n".join(paragraphs), 1000),
            ["\n\n".join(paragraphs[:50]), "\n\n".join(paragraphs[50:])],
        )

    def test_paragraphs_varying_lengths(self):
        paragraphs = ["A" * 500, "B" * 700, "C" * 800]
        self.assertEqual(
            split_paragraph_chunks("\n\n".join(paragraphs), 1000),
            ["A" * 500 + "\n\n" + "B" * 500, "B" * 200 + "\n\n" + "C" * 800],
        )


if __name__ == "__main__":
    unittest.main()
