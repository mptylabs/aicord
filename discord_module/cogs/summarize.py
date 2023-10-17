import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands


from discord_module.utils import load_chat, collect_participants, replace_participants
from gpt_module.main import generate_summary
from misc.utils import split_text_into_chunks


class Summarize(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    summarize = SlashCommandGroup("summarize",
                                  description="Get a quick summary of what's going on in the server."
                                  )

    @summarize.command(description="Get a summary of the channel.")
    async def channel(
            self,
            ctx: discord.ApplicationContext,
            channel: discord.TextChannel,
            interval: str
    ):

        source_messages = await load_chat(channel, interval)

        participants = collect_participants(source_messages)

        conversation = \
            [f"@{message.author.name}: {message.content}" for message in source_messages if message.content]

        summary = generate_summary(conversation)

        chunks = split_text_into_chunks(summary, 2000)
        chunks = [replace_participants(chunk, participants) for chunk in chunks]

        reply = await ctx.edit(content=chunks[0])
        for chunk in chunks[1:]:
            reply = await reply.reply(content=chunk)


def setup(bot):  # try to add argument with settings
    bot.add_cog(Summarize(bot))
