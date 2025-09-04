import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER


@Client.on_message(filters.command("banall", ".") & (filters.me | filters.user(SUDO_USER)))
async def banall_cmd(client: Client, message: Message):
    m = await message.reply_text("🚨 Banall process started...")

    chat_id = message.chat.id
    me = await client.get_chat_member(chat_id, "me")

    # agar bot ke paas rights nahi hai
    if not me.privileges or not me.privileges.can_restrict_members:
        await m.edit("⚠️ Mere paas ban karne ka power nahi hai is group me.")
        return

    count = 0
    async for member in client.get_chat_members(chat_id):
        try:
            if member.user.is_bot or member.user.id == me.user.id:
                continue
            await client.ban_chat_member(chat_id, member.user.id)
            count += 1
            await asyncio.sleep(0.2)  # thoda delay, floodwait avoid
        except Exception:
            pass

    await m.edit(f"✅ Banall complete!\n\nTotal banned: **{count}** members")
