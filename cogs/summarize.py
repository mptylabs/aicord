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
    "You are an expert in summarizing conversations in public text chats.",
    "Your goal is to create a summary of the conversation and extract main topics that were discussed, who started topic and who participated in this topic conversation.",
    "Below you can find the transcript of the conversation:",
    "--------",
    "{text}",
    "--------",
    "",
    "SUMMARY AND TOPIC BULLET LIST WITH THEIR AUTHORS AND PARTICIPANTS:",
)
question_prompt = PromptTemplate.from_template('\n'.join(question_template))

# refine_template = (
#     "You are an expert in summarizing conversations in public text chats.",
#     "Your goal is to create a summary of the conversation and extract main topics that were discussed, who started topic and sho whas involved in this topic conversation.",
#     "We have provided an existing summary up to a certain point: {existing_answer}",
#     "",
#     "Below you can find the transcript of the conversation:",
#     "--------",
#     "{text}",
#     "--------",
#     "",
#     "Given the new context, refine the summary.",
#     "If the context isn't useful, return the original summary.",
#     # "Summary should not be longer than 1800 characters.\n",
#     # "Given the new context, refine the summary and example questions.\n",
#     # "The transcript of the conversation will also be used as the basis for a question and answer bot.\n",
#     # "Provide some examples questions and answers that could be asked about the podcast. Make these questions very specific.\n",
#     # "If the context isn't useful, return the original summary and questions.\n",
#     # "Total output will be a summary of the conversation and a list of example questions the user could ask of the conversation.\n",
#     "",
#     # "SUMMARY AND QUESTIONS:",
#     "SUMMARY AND TOPIC BULLET LIST:",
# )
# refine_prompt = PromptTemplate.from_template('\n'.join(refine_template))

openai_api_key = os.environ['OPENAI_TOKEN']
model_name = "gpt-3.5-turbo-16k"
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    model_name=model_name, 
    # chunk_size=1000, 
    # chunk_overlap=200,
)
chain = load_summarize_chain(
    llm,
    chain_type="stuff",
    prompt=question_prompt,
    # chain_type="refine",
    # question_prompt=question_prompt,
    # refine_prompt=refine_prompt,
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

def split_text_into_chunks(text, max_length):
    """
    Splits a large text into chunks by paragraphs, each chunk being less than the specified length.
    
    Parameters:
        text (str): The text to be split into chunks.
        max_length (int): The maximum length for each chunk.
    
    Returns:
        list: A list of chunks, each less than max_length.
    """
    # Split the text into paragraphs
    paragraphs = text.split("\n\n")
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # Calculate the new length if we add this paragraph and a separator
        new_length = len(current_chunk) + len(paragraph) + len("\n\n")
        
        if new_length <= max_length:
            # If the new chunk is within the limit, append the paragraph
            current_chunk += paragraph + "\n\n"
        else:
            # If the new chunk would be too large, finalize the current chunk and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    # Don't forget to append the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

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

def collect_participants(messages: list[discord.Message]) -> dict[int, str]:
    participants = {}
    for message in messages:
        if message.author.id not in participants:
            participants[message.author.id] = message.author.name

    return participants

def replace_participants(message: str, participants: dict[int, str]) -> str:
    # replace participant name with optional `@` prefix with their mention
    for participant_id, participant_name in participants.items():
        message = message.replace(f"@{participant_name}", f"<@{participant_id}>").replace(f"{participant_name}", f"<@{participant_id}>")
    
    return message

def message_url(message: discord.Message) -> str:
    return f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

class Summarize(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    summarize = SlashCommandGroup("summarize", description="Get a quick summary of what's going on in the server.", guild_ids=[994570645671268442,966090258104062023])

    @summarize.command(description="Get a summary of the current channel.")
    async def here(
        self, 
        ctx: discord.ApplicationContext,
        interval: str
    ):
        source_messages = await load_chat(ctx.channel, interval)

        response = await ctx.respond(f"Found {len(source_messages)} messages. Starting summarization...")

        message_link = f"https://discord.com/channels/{source_messages[0].guild.id}/{source_messages[0].channel.id}/{source_messages[0].id}"

        conversation = [f"<@{message.author.id}>: {message.content}" for message in source_messages if message.content]
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
        debug_data = "Collecting messages...\n\n"

        source_messages = await load_chat(channel, interval)
        debug_data += f"Found {len(source_messages)} messages between {source_messages[0].created_at} and {source_messages[-1].created_at}.\n\n"
        await ctx.edit(content=f"```\n{debug_data}\n```")

        participants = collect_participants(source_messages)

        conversation = [f"@{message.author.name}: {message.content}" for message in source_messages if message.content]
        conversation = '\n\n'.join(conversation)
        documents = text_splitter.create_documents(text_splitter.split_text(conversation))

        debug_data += f"Filtered {len(documents)} documents. Summarizing...\n\n"
        await ctx.edit(content=f"```\n{debug_data}\n```")

        summary = chain.run(documents)
        chunks = split_text_into_chunks(summary, 2000)
        chunks = [replace_participants(chunk, participants) for chunk in chunks]

        reply = await ctx.edit(content=chunks[0])
        for chunk in chunks[1:]:
            reply = await reply.reply(content=chunk)
        

def setup(bot):
    bot.add_cog(Summarize(bot))