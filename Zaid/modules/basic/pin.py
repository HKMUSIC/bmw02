import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

# Pin command
@Client.on_message(filters.command("pin", ".") & (filters.me | filters.user(SUDO_USER)))
async def pin_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to pin it 🚩")
    try:
        await message.reply_to_message.pin(disable_notification=False)
        await message.reply_text("✅ Message pinned!")
        await asyncio.sleep(2)
        await message.delete()  # apna .pin cmd msg delete ho jaye
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Unpin command
@Client.on_message(filters.command("unpin", ".") & (filters.me | filters.user(SUDO_USER)))
async def unpin_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a pinned message to unpin it 🚩")
    try:
        await message.reply_to_message.unpin()
        await message.reply_text("✅ Message unpinned!")
        await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Unpin all command
@Client.on_message(filters.command("unpinall", ".") & (filters.me | filters.user(SUDO_USER)))
async def unpin_all_cmd(client: Client, message: Message):
    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply_text("✅ All messages unpinned!")
        await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
