import unittest
import unittest.mock as mock

from aicord.discord.cogs.summarize import Summarize


class TestSummarize(unittest.TestCase):
    def setUp(self):
        self.bot = mock.Mock()
        self.summarize = Summarize(self.bot)

    def test_load_chat(self):
        channel = mock.Mock()
        interval = "100"
        result = self.summarize.load_chat(channel, interval)
        self.assertIsInstance(result, list)

    def test_summarize_channel(self):
        ctx = mock.Mock()
        channel = mock.Mock()
        interval = "100"
        self.summarize.summarize_channel(ctx, channel, interval)
        ctx.respond.assert_called_once()

    def test_here(self):
        ctx = mock.Mock()
        interval = "100"
        self.summarize.here(ctx, interval)
        ctx.channel.assert_called_once()

    def test_channel(self):
        ctx = mock.Mock()
        channel = mock.Mock()
        interval = "100"
        self.summarize.channel(ctx, channel, interval)
        ctx.respond.assert_called_once()


if __name__ == "__main__":
    unittest.main()
