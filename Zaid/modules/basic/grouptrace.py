from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER
import datetime
import os

SUDO_USERS = SUDO_USER

@Client.on_message(
    filters.command(["grouptrace"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def grouptrace(client: Client, message: Message):
    if not message.chat.type in ["supergroup", "group"]:
        return await message.reply_text("❌ This command only works in groups.")

    chat = await client.get_chat(message.chat.id)

    # Group basic info
    title = chat.title
    group_id = chat.id

    # Creation date (approx - Telegram IDs are snowflakes)
    try:
        created_time = datetime.datetime.fromtimestamp(
            int(str(group_id)[-10:])
        )
        old = created_time.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        old = "Unknown"

    # Members count
    members = await client.get_chat_members_count(chat.id)

    # Admins count + owner
    admins = []
    owner = "Unknown"
    async for admin in client.get_chat_members(chat.id, filter="administrators"):
        admins.append(admin)
        if admin.status == "creator":
            owner = f"{admin.user.first_name} ({admin.user.id})"
    admin_count = len(admins)

    # Invite link
    try:
        link = chat.invite_link or (await client.export_chat_invite_link(chat.id))
    except Exception:
        link = "No link available"

    # Final text
    text = f"""
📛 **Group Name:** {title}
🆔 **Group ID:** `{group_id}`
🕐 **Created On:** {old}
👑 **Owner:** {owner}
👥 **Members:** {members}
🛡️ **Admins:** {admin_count}
🌐 **Invite Link:** {link}
    """

    # Profile photo download
    if chat.photo:
        photo_path = f"{chat.id}_pic.jpg"
        await client.download_media(chat.photo.big_file_id, file_name=photo_path)
        await message.reply_photo(photo=photo_path, caption=text)
        os.remove(photo_path)
    else:
        await message.reply_text(text)
