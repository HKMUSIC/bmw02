import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

SUDO_USERS = SUDO_USER


# 🔹 Pin command
@Client.on_message(filters.command("pin", ".") & (filters.me | filters.user(SUDO_USERS)))
async def pin_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply karke use karo: `.pin`")

    if message.chat.type not in ("group", "supergroup", "channel"):
        return await message.reply_text("⚠️ Ye command sirf groups/supergroups/channels me kaam karti hai.")

    try:
        await client.pin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.id,
            both_sides=True  # har member ke liye show hoga
        )
        await message.reply_text("📌 Message successfully pinned!")
    except Exception as e:
        await message.reply_text(f"❌ Pin failed: `{e}`")


# 🔹 Unpin command
@Client.on_message(filters.command("unpin", ".") & (filters.me | filters.user(SUDO_USERS)))
async def unpin_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply karke use karo: `.unpin`")

    if message.chat.type not in ("group", "supergroup", "channel"):
        return await message.reply_text("⚠️ Ye command sirf groups/supergroups/channels me kaam karti hai.")

    try:
        await client.unpin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
        await message.reply_text("✅ Message successfully unpinned!")
    except Exception as e:
        await message.reply_text(f"❌ Unpin failed: `{e}`")


# 🔹 Unpinall command
@Client.on_message(filters.command("unpinall", ".") & (filters.me | filters.user(SUDO_USERS)))
async def unpin_all_cmd(client: Client, message: Message):
    if message.chat.type not in ("group", "supergroup", "channel"):
        return await message.reply_text("⚠️ Ye command sirf groups/supergroups/channels me kaam karti hai.")

    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply_text("🧹 All pinned messages removed successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Unpin all failed: `{e}`")
