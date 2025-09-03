from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

@Client.on_message(
    filters.command(["leave", "leaveme"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def leave_group(client: Client, message: Message):
    """ Leave Group/Channel """
    chat = message.chat

    if chat.type in ["supergroup", "group", "channel"]:
        await message.reply_text(f"👋 Leaving **{chat.title}** ...")
        try:
            await client.leave_chat(chat.id)
        except Exception as e:
            await message.reply_text(f"❌ Error while leaving: {e}")
    else:
        await message.reply_text("⚠️ This command only works in groups/channels.")
