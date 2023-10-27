import asyncio

from dotenv import load_dotenv

from aicord.discord.bot import main


if __name__ == "__main__":

    load_dotenv()
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        pass
