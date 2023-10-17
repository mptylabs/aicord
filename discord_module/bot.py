from __future__ import annotations

from discord import Bot, Intents

from discord_module.cogs import COGS
from configs.config import settings, DiscordSettings


class AicordBot(Bot):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.guild_messages = True  # maybe need fix
        intents.message_content = True
        super().__init__(intents=intents)

        self.config: DiscordSettings = settings.discord

    def run(self) -> None:
        raise NotImplementedError("Please use `.start()` instead.")
    
    async def start(self) -> None:
        await super().start(self.config.token)


async def run_bot() -> None:

    bot = AicordBot()

    for cog in COGS:
        bot.load_extension(cog.name)

    await bot.start()
