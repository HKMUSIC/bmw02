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

    bot = "Gojo_Hack49bot"

    try:
        await client.send_message(bot, f"tg{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"tg{user.id}")

    await asyncio.sleep(3)

    try:
        async for response in client.get_chat_history(bot, limit=1):
            try:
                # Try copying the message
                await response.copy(message.chat.id)
            except Exception:
                # If copy fails → forward instead
                await client.forward_messages(message.chat.id, bot, response.id)

            # Add footer
            await client.send_message(
                message.chat.id, "ᴘᴏᴡᴇʀᴇᴅ - 🇹𝐇𝐄🇧𝐌𝐖🖤"
            )
            await status.delete()
            return

        await status.edit("❌ No response received from the bot.")

    except Exception as e:
        return await status.edit(f"⚠️ Error while fetching: {e}")


# Add help command
add_command_help(
    "numinfo",
    [
        [
            "numinfo [reply/userid/username]",
            "Fetches number info & name history by querying external bot.",
        ],
    ],
      )
          
