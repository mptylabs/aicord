import datetime
import os

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from duration_parser import parse as parse_duration

from langchain import PromptTemplate
from langchain.schema import Document, BaseMessage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_loaders import base as chat_loaders
from langchain.chat_loaders.utils import (
    map_ai_messages,
    merge_chat_runs,
)

question_template = (
    "You are an expert in summarizing conversations in public text chats.\n",
    "Your goal is to create a summary of the conversation and extract main topics that were discussed, who started topic and sho whas involved in this topic conversation.\n",
    "Below you can find the transcript of the conversation:\n",
    "--------\n",
    "{text}\n",
    "--------\n",
    # "\n",
    # "The transcript of the conversation will also be used as the basis for a question and answer bot.\n",
    # "Provide some examples questions and answers that could be asked about the podcast. Make these questions very specific.\n",
    # "\n",
    # "Total output will be a summary of the conversation and a list of example questions the user could ask of the conversation.\n"
    "\n",
    # "SUMMARY AND QUESTIONS:",
    "CONCISE SUMMARY:",
)
question_prompt = PromptTemplate.from_template(''.join(question_template))

refine_template = (
    "You are an expert in summarizing conversations in public text chats.\n",
    "Your goal is to create a summary of the conversation and extract main topics that were discussed, who started topic and sho whas involved in this topic conversation.\n",
    "We have provided an existing summary up to a certain point: {existing_answer}\n",
    "\n",
    "Below you can find the transcript of the conversation:\n",
    "--------\n",
    "{text}\n",
    "--------\n",
    "\n",
    "Given the new context, refine the summary\.\n",
    "If the context isn't useful, return the original summary.\n",
    # "Given the new context, refine the summary and example questions.\n",
    # "The transcript of the conversation will also be used as the basis for a question and answer bot.\n",
    # "Provide some examples questions and answers that could be asked about the podcast. Make these questions very specific.\n",
    # "If the context isn't useful, return the original summary and questions.\n",
    # "Total output will be a summary of the conversation and a list of example questions the user could ask of the conversation.\n",
    "\n",
    # "SUMMARY AND QUESTIONS:",
    "CONCISE SUMMARY:",
)
refine_prompt = PromptTemplate.from_template(''.join(refine_template))

openai_api_key = os.environ['OPENAI_TOKEN']
model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name=model_name, chunk_size=1000, chunk_overlap=200)
chain = load_summarize_chain(
    llm,
    chain_type="refine",
    # prompt=question_prompt,
    question_prompt=question_prompt,
    refine_prompt=refine_prompt,
    verbose=True,
)

# def map_message(message: discord.Message) -> BaseMessage:
#     return HumanMessage(
#         content=message.content,
#         additional_kwargs={
#             "sender": message.author.id,
#             "events": [{"message_time": message.created_at}],
#         },
#     )

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

class Summarize(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    summarize = SlashCommandGroup("summarize", description="Get a quick summary of what's going on in the server.")

    @summarize.command(description="Get a summary of the current channel.")
    async def here(
        self, 
        ctx: discord.ApplicationContext,
        interval: str
    ):
        source_messages = await load_chat(ctx.channel, interval)

        response = await ctx.respond(f"Found {len(source_messages)} messages. Starting summarization...")

        message_link = f"https://discord.com/channels/{source_messages[0].guild.id}/{source_messages[0].channel.id}/{source_messages[0].id}"

        conversation = [f"{message.author.name}: {message.content}" for message in source_messages if message.content]
        conversation = '\n\n'.join(conversation)
        documents = text_splitter.create_documents(text_splitter.split_text(conversation))

        await ctx.edit(content=f"Filtered {len(documents)} documents. Summarizing... \n First message: {message_link}")

        summary = chain.run(documents)

        print(summary)

        await ctx.edit(content=summary)

    @summarize.command(description="Get a summary of the channel.")
    async def channel(
        self, 
        ctx: discord.ApplicationContext,
        channel: discord.TextChannel,
        interval: str
    ):
        source_messages = await load_chat(channel, interval)

        response = await ctx.respond(f"Found {len(source_messages)} messages. Starting summarization...")

        message_link = f"https://discord.com/channels/{source_messages[0].guild.id}/{source_messages[0].channel.id}/{source_messages[0].id}"

        conversation = [f"{message.author.name}: {message.content}" for message in source_messages if message.content]
        conversation = '\n\n'.join(conversation)
        documents = text_splitter.create_documents(text_splitter.split_text(conversation))

        await ctx.edit(content=f"Filtered {len(documents)} documents. Summarizing... \n First message: {message_link}")

        summary = chain.run(documents)

        print(summary)

        await ctx.edit(content=summary)
        

def setup(bot):
    bot.add_cog(Summarize(bot))