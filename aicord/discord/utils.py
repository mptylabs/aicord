from __future__ import annotations

import discord


def collect_participants(messages: list[discord.Message]) -> dict[int, str]:
    participants = {}
    for message in messages:
        if message.author.id not in participants:
            participants[message.author.id] = message.author.name

    return participants


def replace_participants(message: str, participants: dict[int, str]) -> str:
    """
    Replace participant name with optional `@` prefix with their mention
    """
    for participant_id, participant_name in participants.items():
        message = (message
                   .replace(f"@{participant_name}", f"<@{participant_id}>")
                   .replace(f"{participant_name}", f"<@{participant_id}>"))

    return message
