import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER


@Client.on_message(filters.command("owner", ".") & (filters.me | filters.user(SUDO_USER)))
async def owner_cmd(client: Client, message: Message):
    frames = [
        "🚁........",
        "🚁.........😎",
        "🚁.......😎",
        "🚁.....😎",
        "🚁...😎",
        "🚁😎  (𝐋𝐚𝐧𝐝𝐢𝐧𝐠...)",

        "😎🪂 (𝐉𝐮𝐦𝐩𝐢𝐧𝐠 𝐝𝐨𝐰𝐧...)",

        "😎🔥 (𝐖𝐚𝐥𝐤𝐢𝐧𝐠 𝐰𝐢𝐭𝐡 𝐚𝐭𝐭𝐢𝐭𝐮𝐝𝐞...)",

        "💀 𝐇𝐄𝐇𝐄 𝐋𝐎𝐃𝐄...",
        "💀 𝐇𝐄𝐇𝐄 𝐋𝐎𝐃𝐄 𝐀𝐔𝐊𝐀𝐓 𝐌𝐀𝐈 𝐍𝐇𝐈...",
        "💀 𝐇𝐄𝐇𝐄 𝐋𝐎𝐃𝐄 𝐀𝐔𝐊𝐀𝐓 𝐌𝐀𝐈 𝐍𝐇𝐈 𝐓𝐇𝐎 𝐂𝐇𝐎𝐃𝐔 𝐆𝐇𝐀...",
        "💀 𝐇𝐄𝐇𝐄 𝐋𝐎𝐃𝐄 𝐀𝐔𝐊𝐀𝐓 𝐌𝐀𝐈 𝐍𝐇𝐈 𝐓𝐇𝐎 𝐂𝐇𝐎𝐃𝐔 𝐆𝐇𝐀 𝐆𝐇𝐀𝐓 𝐌𝐀𝐈...",
        "💀 𝐇𝐄𝐇𝐄 𝐋𝐎𝐃𝐄 𝐀𝐔𝐊𝐀𝐓 𝐌𝐀𝐈 𝐍𝐇𝐈 𝐓𝐇𝐎 𝐂𝐇𝐎𝐃𝐔 𝐆𝐇𝐀 𝐆𝐇𝐀𝐓 𝐌𝐀𝐈 😏",
        "🔥 ˹𝐁ᴍᴡ 𝐊𝐎 𝐏𝐀𝐏𝐀 𝐁𝐎𝐋𝐎",
        "🔥 ˹𝐁ᴍᴡ 𝐊𝐎 𝐏𝐀𝐏𝐀 𝐁𝐎𝐋𝐎 𝐃𝐌 𝐌𝐀𝐈 @BMW0RACER",
    ]

    m = await message.reply_text("🚁 𝐂𝐚𝐥𝐥𝐢𝐧𝐠 𝐎𝐰𝐧𝐞𝐫...")

    for frame in frames:
        await m.edit(frame)
        await asyncio.sleep(0.7)
