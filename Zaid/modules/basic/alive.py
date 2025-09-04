from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER

SUDO_USERS = SUDO_USER

@Client.on_message(
    filters.command(["alive"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def alive(client: Client, message: Message):
    """ Alive / Status Check """
    text = """
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
   ✦ 𝑩𝑴𝑾 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ✦
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

🔥 𝐈 𝐀𝐌 𝐀𝐋𝐈𝐕𝐄 & 𝐊𝐈𝐍𝐆𝐒 𝐍𝐄𝐕𝐄𝐑 𝐃𝐈𝐄 🔥  

⚡ 𝐀𝐓𝐓𝐈𝐓𝐔𝐃𝐄 𝐎𝐍 𝐅𝐈𝐑𝐄 ⚡  
🚀 𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 : 𝑩𝑴𝑾 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 🚀
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
"""
    await message.reply_text(text)
