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
    result = f"📊 Multiplication Table of {num} 📊\n\n"
    m = await message.reply_text("📊 Generating table...")

    for i in range(1, 11):
        result += f"{num} × {i} = {num * i}\n"
        await m.edit_text(result)
        await asyncio.sleep(0.5)  # delay for smooth effect
