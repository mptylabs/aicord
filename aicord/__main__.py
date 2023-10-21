from __future__ import annotations

import asyncio
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    from aicord.discord.bot import main

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass