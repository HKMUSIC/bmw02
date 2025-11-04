import asyncio

from pyrogram import Client, filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import Message

from Zaid.modules.help import add_command_help
from Zaid.modules.basic.profile import extract_user


@Client.on_message(filters.command(["numinfo", "getnum"], ".") & filters.me)
async def numinfo(client: Client, message: Message):
    args = await extract_user(message)
    status = await message.edit_text("`Processing...`")

    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await status.edit("`Please specify a valid user!`")
    else:
        return await status.edit("`Reply to a user or give userid/username!`")
    bot = "istalk_nukbrr_uhjdg_sms_bot"

    try:
        await client.send_message(bot, f"tg{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"tg{user.id}")

    # Wait a few seconds for the bot to respond
    await asyncio.sleep(3)

    final_text = None

    async for msg in client.get_chat_history(bot, limit=10):
        if not msg.from_user or not msg.from_user.is_bot or not msg.text:
            continue

        text = msg.text

        # Check if this bot message contains the same user.id
        if str(user.id) not in text:
            continue

        # Handle bot limit message
        if "⚠️ Ваш лимит запросов временно исчерпан." in text:
            final_text = (
                "❌ Sorry, you have exceeded your free requests for today.\n"
                "Wait for them to refill."
            )
            break

        # Handle normal reply starting with 💬 ID
        if text.startswith("💬 ID"):
            # Replace Телефон → Phone
            text = text.replace("Телефон:", "𝗣𝗛𝗢𝗡𝗘[:](https://files.catbox.moe/vfbhn2.jpg)")
            # Replace История изменения имени → Thank you for Using Me
            text = text.replace("💬 ID:", "ᴜsᴇʀ ɪᴅ [-](https://files.catbox.moe/vfbhn2.jpg)")
            text = text.replace("🕓 История изменения имени:", "\n<pre>ɪsᴋᴀ ᴋᴜᴄʜ ɴᴀ ɴɪᴋʟᴀ ʙʜᴀɪ 💪💀</pre>\n")
            text = text.replace("👁 Интересовались этим:", "ᴘᴇᴏᴘʟᴇ ɪɴᴛʀᴇsᴛᴇᴅ-")
            # Take only first 4 lines
            lines = text.splitlines()[:4]
            final_text = "\n".join(lines)
            break

    if not final_text:
        return await status.edit("❌ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗟𝗶𝗺𝗶𝘁 𝗛𝗶𝘁[!](https://files.catbox.moe/vfbhn2.jpg)\n\nʏᴏᴜ’ᴠᴇ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ᴍᴀxᴇᴅ ᴏᴜᴛ ʏᴏᴜʀ ғʀᴇᴇ ʀᴇǫᴜᴇsᴛs. sɪᴛ ᴛɪɢʜᴛ, ʟᴇᴛ ᴛʜᴇᴍ ʀᴇғɪʟʟ, ᴀɴᴅ ᴄᴏᴍᴇ ʙᴀᴄᴋ sᴛʀᴏɴɢᴇʀ! 😎\n\n•─────────────────•\nᴘᴏᴡєʀєᴅ ʙʏ» [愛|𝗦𝗧么𝗟𝗞𝚵𝗥](https://t.me/hehe_stalker)\n•─────────────────•")

    # Add footer
    final_text += "<pre>ғᴏʀ ᴇᴅᴜᴄᴀᴛɪᴏɴᴀʟ ᴘᴜʀᴘᴏsᴇs ᴏɴʟʏ ⚠️</pre>\n•─────────────────•\nᴘᴏᴡєʀєᴅ ʙʏ » [愛|𝗦𝗧么𝗟𝗞𝚵𝗥](https://t.me/hehe_stalker)\n•─────────────────•"

    await client.send_message(message.chat.id, final_text)
    await status.delete()


# Add help command
add_command_help(
    "numinfo",
    [
        [
            "numinfo [reply/userid/username]",
            "Fetches number info & name history by querying external bot (first 4 lines only, with 'Phone').",
        ],
    ],
          )
      
