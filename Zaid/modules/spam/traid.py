import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Database imports
from cache.data import *
from Zaid.database.rraid import *
from Zaid import SUDO_USER

SUDO_USERS = SUDO_USER
ACTIVE_TRAIDS = {} # Group wise target store karne ke liye

@Client.on_message(
    filters.command(["traid", "untraid"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def traid_cmd(xspam: Client, e: Message):
    cmd = e.command[0]
    chat_id = e.chat.id
    
    if cmd == "traid":
        args = e.text.split(maxsplit=1)
        target_user = None
        
        if e.reply_to_message:
            target_user = e.reply_to_message.from_user.id
        elif len(args) > 1:
            target_user = args[1]
        else:
            return await e.reply_text("ᴜsᴀɢᴇ: `.ᴛʀᴀɪᴅ @ᴜsᴇʀɴᴀᴍᴇ` / `ᴜsᴇʀɪᴅ` ᴏʀ ʀᴇᴘʟʏ")
            
        try:
            user = await xspam.get_users(target_user)
            user_id = user.id
        except Exception:
            return await e.reply_text("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ.")

        if int(user_id) in VERIFIED_USERS or int(user_id) in SUDO_USERS:
            return await e.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴛʀᴀɪᴅ ᴛʜɪs ᴜsᴇʀ.")
            
        # Target ki last message ID track karne ke liye system
        ACTIVE_TRAIDS[chat_id] = {"target_id": user_id, "last_msg_id": None}
        await e.reply_text(f"ᴛʀᴀɪᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! Ab aap jo bhi likhenge wo us user ko reply jayega.")
        
    elif cmd == "untraid":
        if chat_id in ACTIVE_TRAIDS:
            del ACTIVE_TRAIDS[chat_id]
            await e.reply_text("ᴛʀᴀɪᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ.")

# Ye watcher target ki latest message ID save karta rahega
@Client.on_message(filters.group, group=9)
async def target_message_tracker(xspam: Client, e: Message):
    chat_id = e.chat.id
    if chat_id in ACTIVE_TRAIDS:
        if e.from_user and e.from_user.id == ACTIVE_TRAIDS[chat_id]["target_id"]:
            ACTIVE_TRAIDS[chat_id]["last_msg_id"] = e.id

# Ye watcher aapke message ko reply me convert karega
@Client.on_message(filters.me & filters.group, group=10)
async def traid_reply_handler(xspam: Client, e: Message):
    chat_id = e.chat.id
    
    if chat_id not in ACTIVE_TRAIDS or e.text.startswith("."):
        return
        
    target_data = ACTIVE_TRAIDS[chat_id]
    target_msg_id = target_data["last_msg_id"]
    
    # Agar target ne abhi tak koi msg nahi kiya group me, toh skip
    if not target_msg_id:
        return

    try:
        # Aapka bheja hua simple message delete karega
        await e.delete()
        # Wahi message target ke message par reply banke jayega
        await xspam.send_message(
            chat_id, 
            e.text, 
            reply_to_message_id=target_msg_id
        )
    except Exception as err:
        print(f"Error in Traid Reply: {err}")
        
