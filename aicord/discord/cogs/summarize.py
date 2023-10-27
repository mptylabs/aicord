import datetime
import os

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from duration_parser import parse as parse_duration

from aicord.discord.utils import collect_participants, replace_participants
from aicord.utils.string import split_paragraph_chunks
from aicord.core.ai.summarize import chain, text_splitter

class Summarize(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
    if not os.environ.get('GUILD_IDS'):
        guild_ids = None
    else:
        guild_ids = os.environ.get('GUILD_IDS')

    summarize = SlashCommandGroup("summarize",
                                  description="Get a quick summary of what's going on in the server.",
                                  guild_ids=guild_ids)

    @staticmethod
    async def load_chat(channel: discord.TextChannel, interval: str) -> list[discord.Message]:
        if interval.isdigit():
            source_messages = await channel.history(
                limit=int(interval),
                oldest_first=True,
            ).flatten()
        else:
            after = datetime.datetime.now() - datetime.timedelta(seconds=parse_duration(interval))
            source_messages = await channel.history(
                after=after,
                limit=10000,
                oldest_first=True,
            ).flatten()

        return source_messages

    async def summarize_channel(
            self,
            ctx: discord.ApplicationContext,
            channel: discord.TextChannel,
            interval: str
    ):
        await ctx.respond(f"Summarizing {channel.mention}...")
        source_messages = await self.load_chat(channel, interval)
        participants = collect_participants(source_messages)

        conversation = [f"@{message.author.name}: {message.content}" for message in source_messages if message.content]
        conversation = '\n\n'.join(conversation)
        documents = text_splitter.create_documents(text_splitter.split_text(conversation))

        summary = replace_participants(chain.run(documents), participants)
        chunks = split_paragraph_chunks(summary, 2000)
        chunks = [replace_participants(chunk, participants) for chunk in chunks]

        reply = await ctx.edit(content=chunks[0])
        for chunk in chunks[1:]:
            reply = await reply.reply(content=chunk)

    @summarize.command(description="Get a summary of the current channel.")
    async def here(
        self, 
        ctx: discord.ApplicationContext,
        interval: str
    ):
        await self.summarize_channel(ctx, ctx.channel, interval)

    @summarize.command(description="Get a summary of the channel.")
    async def channel(
        self, 
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        interval: str
    ):
        await self.summarize_channel(ctx, channel, interval)
        

def setup(bot):
    bot.add_cog(Summarize(bot))