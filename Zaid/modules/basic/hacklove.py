import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

@Client.on_message(filters.command("hacklove", ".") & (filters.me | filters.user(SUDO_USER)))
async def hacklove_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `.hacklove <username>`")
        return
    
    target = message.command[1]
    m = await message.reply_text(f"💻 Hacking into {target}’s heart...")

    progress = [
        "[▒▒▒▒▒▒▒▒▒▒] 0%",
        "[▓▒▒▒▒▒▒▒▒▒] 10%",
        "[▓▓▒▒▒▒▒▒▒▒] 20%",
        "[▓▓▓▒▒▒▒▒▒▒] 30%",
        "[▓▓▓▓▒▒▒▒▒▒] 40%",
        "[▓▓▓▓▓▒▒▒▒▒] 50%",
        "[▓▓▓▓▓▓▒▒▒▒] 60%",
        "[▓▓▓▓▓▓▓▒▒▒] 70%",
        "[▓▓▓▓▓▓▓▓▒▒] 80%",
        "[▓▓▓▓▓▓▓▓▓▒] 90%",
        "[▓▓▓▓▓▓▓▓▓▓] 100%"
    ]

    for p in progress:
        await m.edit_text(f"💻 Hacking into {target}’s heart...\n\n{p}")
        await asyncio.sleep(0.4)

    love_percent = random.randint(10, 110)  # Random funny love %
    result = f"""
❤️ Hacklove Result ❤️

Target: {target}
Love Detected: {love_percent}%

{"🔥 Perfect Couple 🔥" if love_percent > 80 else "💔 Better luck next time 😂"}
"""
    await m.edit_text(result)
