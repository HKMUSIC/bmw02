from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from Zaid import SUDO_USER

@Client.on_message(
    filters.command(["spamemoji"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def spamemoji(client: Client, message: Message):
    """ Emoji Spam in Chat or Reply Mode """
    args = message.text.split(maxsplit=2)

    if len(args) < 3 and not message.reply_to_message:
        return await message.reply_text("❌ Usage: `.spamemoji {count} {emoji}` (or reply to a user)")

    try:
        count = int(args[1]) if len(args) > 1 else int(message.text.split()[1])
        emoji = args[2] if len(args) > 2 else message.text.split()[2]
    except Exception:
        return await message.reply_text("❌ Count must be a number!")

    # --- REPLY MODE (DM SPAM) ---
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        ok = await client.get_users(user_id)
        target_id = ok.id

        await message.reply_text(f"🚀 Emoji DM Spam Started\nSending {emoji} {count} times to {ok.first_name}")

        for _ in range(count):
            await client.send_message(target_id, emoji)
            await asyncio.sleep(0.10)

    # --- NORMAL CHAT MODE ---
    else:
        await message.reply_text(f"🚀 Emoji Spam Started\nSpamming {count} times with {emoji}")

        for _ in range(count):
            await client.send_message(message.chat.id, emoji)
            await asyncio.sleep(0.10)
