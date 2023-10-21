from __future__ import annotations

from typing import TypedDict

import os

import discord

from aicord.discord.cogs import COGS


class BotConfig(TypedDict, total=False):
    owner_ids: list[int]
    owner_guild_ids: list[int]


class AicordBot(discord.Bot):
    def __init__(self, config: BotConfig) -> None:
        intents = discord.Intents.default()

        super().__init__(intents=intents)

        self.config: BotConfig = config

    def run(self) -> None:
        raise NotImplementedError("Please use `.start()` instead.")

    async def start(self) -> None:
        await super().start(os.environ['DISCORD_TOKEN'])


async def main() -> None:
    owner_guild_ids = [int(guild_id) for guild_id in os.environ['OWNER_GUILD_IDS'].split(',')]
    owner_ids = [int(owner_id) for owner_id in os.environ['OWNER_IDS'].split(',')]

    config = BotConfig(
        owner_ids=owner_ids,
        owner_guild_ids=owner_guild_ids
    )

    bot = AicordBot(config)

    for cog in COGS:
        bot.load_extension(cog.name)

    await bot.start()
    print("Bot started.")
