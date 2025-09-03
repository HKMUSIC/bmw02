from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from Zaid import SUDO_USER

@Client.on_message(
    filters.command(["seen"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def seen(client: Client, message: Message):
    """ Check Last Seen of a User """
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("❌ Usage: `.seen {username}` or reply to a user")

    try:
        if message.reply_to_message:
            user = await client.get_users(message.reply_to_message.from_user.id)
        else:
            username = message.command[1]
            user = await client.get_users(username)

        if user.status:  # status mil gaya
            if hasattr(user.status, "was_online"):
                last_seen = user.status.was_online.strftime("%Y-%m-%d %H:%M:%S")
                await message.reply_text(f"👤 Last seen of {user.first_name} (`{user.id}`):\n📅 `{last_seen}`")
            else:
                await message.reply_text(f"👤 Last seen of {user.first_name} (`{user.id}`): {user.status}")
        else:
            await message.reply_text("⚠️ User ka last seen hidden hai ya unavailable hai.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
