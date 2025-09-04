import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

# Ban All Members (except you & SUDO_USER)
@Client.on_message(filters.command("banall", ".") & (filters.me | filters.user(SUDO_USER)))
async def ban_all(client: Client, message: Message):
    chat_id = message.chat.id
    me = await client.get_me()

    # Confirmation
    confirm = await message.reply_text("⚠️ Are you sure you want to **BAN ALL** members? Reply `yes` within 10 sec.")
    try:
        reply = await client.listen(chat_id, filters=filters.text & filters.user(message.from_user.id), timeout=10)
    except:
        await confirm.edit("❌ Cancelled banall.")
        return
    
    if reply.text.lower() != "yes":
        await confirm.edit("❌ Cancelled banall.")
        return

    await confirm.edit("🚀 Starting BAN ALL members...")

    async for member in client.get_chat_members(chat_id):
        if member.user.is_self or member.user.id == SUDO_USER:
            continue  # skip yourself & sudo user
        try:
            await client.ban_chat_member(chat_id, member.user.id)
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"Error banning {member.user.id}: {e}")

    await confirm.edit("✅ Banall completed (excluded self & sudo).")

# Kick All Members (except you & SUDO_USER)
@Client.on_message(filters.command("kickall", ".") & (filters.me | filters.user(SUDO_USER)))
async def kick_all(client: Client, message: Message):
    chat_id = message.chat.id
    me = await client.get_me()

    confirm = await message.reply_text("⚠️ Are you sure you want to **KICK ALL** members? Reply `yes` within 10 sec.")
    try:
        reply = await client.listen(chat_id, filters=filters.text & filters.user(message.from_user.id), timeout=10)
    except:
        await confirm.edit("❌ Cancelled kickall.")
        return
    
    if reply.text.lower() != "yes":
        await confirm.edit("❌ Cancelled kickall.")
        return

    await confirm.edit("🚀 Starting KICK ALL members...")

    async for member in client.get_chat_members(chat_id):
        if member.user.is_self or member.user.id == SUDO_USER:
            continue  # skip yourself & sudo user
        try:
            await client.ban_chat_member(chat_id, member.user.id)   # ban
            await client.unban_chat_member(chat_id, member.user.id) # unban (kick effect)
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"Error kicking {member.user.id}: {e}")

    await confirm.edit("✅ Kickall completed (excluded self & sudo).")
