from __future__ import annotations

from typing import TypedDict

import asyncio
import os
from dotenv import load_dotenv

import discord

from cogs import COGS

load_dotenv()

owner_guild_ids = [int(id) for id in os.environ['OWNER_GUILD_IDS'].split(',')]
owner_ids = [int(id) for id in os.environ['OWNER_IDS'].split(',')]

intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True

class BotConfig(TypedDict, total=False):
    owner_ids: list[int]
    owner_guild_ids: list[int]

class AicordBot(discord.Bot):
    def __init__(self, config: BotConfig) -> None:
        super().__init__()

        self.config: BotConfig = config

    def run(self) -> None:
        raise NotImplementedError("Please use `.start()` instead.")
    
    async def start(self) -> None:
        await super().start(os.environ['DISCORD_TOKEN'])

async def main() -> None:
    config = BotConfig(
        owner_ids=owner_ids,
        owner_guild_ids=owner_guild_ids
    )

    bot = AicordBot(config)

    for cog in COGS:
        bot.load_extension(cog.name)

    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())