import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

@Client.on_message(filters.command("table", ".") & (filters.me | filters.user(SUDO_USER)))
async def table_cmd(client: Client, message: Message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.reply_text("Usage: `.table <number>`")
        return
    
    num = int(args[1])
    header = f"📊 Multiplication Table of {num} 📊\n\n"
    m = await message.reply_text("⌛ Generating table...")

    result = header
    for i in range(1, 11):
        line = f"{num} × {i} = {num * i}\n"
        for j in range(len(line)):
            await m.edit_text(result + line[:j+1])   # typewriter effect
            await asyncio.sleep(0.05)  # typing speed per character
        result += line
        await asyncio.sleep(0.3)  # small pause before next line
