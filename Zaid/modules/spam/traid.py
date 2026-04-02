import asyncio
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message

# Importing required variables from your bot's database
from cache.data import *
from Zaid.database.rraid import *
from Zaid import SUDO_USER

SUDO_USERS = SUDO_USER
TRAID_USERS = []

@Client.on_message(
    filters.command(["traid", "untraid"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def traid_cmd(xspam: Client, e: Message):
    cmd = e.command[0]
    args = e.text.split(maxsplit=1)
    
    target_user = None
    
    # Agar message ko reply kiya hai
    if e.reply_to_message:
        target_user = e.reply_to_message.from_user.id
    # Agar command ke aage @username ya userid diya hai
    elif len(args) > 1:
        target_user = args[1]
    else:
        return await e.reply_text("ᴜsᴀɢᴇ: `.ᴛʀᴀɪᴅ @ᴜsᴇʀɴᴀᴍᴇ` / `ᴜsᴇʀɪᴅ` ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ.\nᴛᴏ sᴛᴏᴘ: `.ᴜɴᴛʀᴀɪᴅ @ᴜsᴇʀɴᴀᴍᴇ`")
        
    try:
        # Pyrogram khud username ya id se user ki details nikal lega
        user = await xspam.get_users(target_user)
        user_id = user.id
    except Exception:
        return await e.reply_text("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ ᴏʀ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")

    if cmd == "traid":
        if int(user_id) in VERIFIED_USERS:
            return await e.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴛʀᴀɪᴅ ᴠᴇʀɪғɪᴇᴅ ᴜsᴇʀs 😈")
        elif int(user_id) in SUDO_USERS:
            return await e.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴛʀᴀɪᴅ sᴜᴅᴏ ᴜsᴇʀs 🛡️")
            
        if user_id not in TRAID_USERS:
            TRAID_USERS.append(user_id)
        await e.reply_text(f"ᴛʀᴀɪᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴏɴ {user.first_name} 😈 (ɢʟᴏʙᴀʟʟʏ)")
        
    elif cmd == "untraid":
        if user_id in TRAID_USERS:
            TRAID_USERS.remove(user_id)
            await e.reply_text(f"ᴛʀᴀɪᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ {user.first_name} 🤫")
        else:
            await e.reply_text("ᴛʀᴀɪᴅ ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ ᴏɴ ᴛʜɪs ᴜsᴇʀ.")

# Watcher background me hamesha active rahega
@Client.on_message(~filters.me & filters.group, group=10)
async def traid_watcher(xspam: Client, e: Message):
    if not e.from_user:
        return
    
    # Ab ye sirf user_id check karega, matlab kisi bhi group me kaam karega
    if e.from_user.id in TRAID_USERS:
        reply_msg = choice(HIRAID) 
        
        await asyncio.sleep(0.10)
        await e.reply_text(reply_msg)
        
