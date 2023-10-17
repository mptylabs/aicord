from discord import TextChannel, Message
from datetime import datetime, timedelta
from duration_parser import parse as parse_duration


async def load_chat(channel: TextChannel, interval: str) -> list[Message]:
    if interval.isdigit():
        source_messages = await channel.history(
            limit=int(interval),
            oldest_first=True,
        ).flatten()
    else:
        after = datetime.now() - timedelta(seconds=parse_duration(interval))
        source_messages = await channel.history(
            after=after,
            limit=10000,
            oldest_first=True,
        ).flatten()

    return source_messages


def collect_participants(messages: list[Message]) -> dict[int, str]:
    participants = {}
    for message in messages:
        if message.author.id not in participants:
            participants[message.author.id] = message.author.name

    return participants

def message_url(message: Message) -> str:
    return f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"


def replace_participants(message: str, participants: dict[int, str]) -> str:
    # replace participant name with optional `@` prefix with their mention
    for participant_id, participant_name in participants.items():
        message = message.replace(f"@{participant_name}", f"<@{participant_id}>").replace(f"{participant_name}",
                                                                                          f"<@{participant_id}>")

    return message