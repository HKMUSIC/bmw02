import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

SUDO_USERS = SUDO_USER

@Client.on_message(filters.command("pin", ".") & (filters.me | filters.user(SUDO_USERS)))
async def pin_cmd(client: Client, message: Message):
    # Must be used as a reply
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply karke use karo: `.pin` (ya `.pin notify`)")

    # Only works in groups/supergroups/channels
    if message.chat.type not in ("group", "supergroup", "channel"):
        return await message.reply_text("⚠️ Ye command sirf groups/supergroups/channels me kaam karti hai.")

    # Parse mode: silent (default) or notify
    args = message.text.split(maxsplit=1)
    notify = False
    if len(args) > 1 and args[1].strip().lower() in ("notify", "alert"):
        notify = True

    try:
        await client.pin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.id,
            disable_notification=not notify  # True = silent pin
        )
        status = "🔔 Notified" if notify else "🤫 Silent"
        await message.reply_text(f"📌 Pinned! ({status})")
    except Exception as e:
        # Common reasons: not admin / no can_pin_messages permission
        await message.reply_text(f"❌ Pin failed: `{e}`")
