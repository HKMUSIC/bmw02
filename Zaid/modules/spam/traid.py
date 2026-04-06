import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# Database imports (Apne paths yahan daal lena)
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
            user_mention = user.mention # HTML mention store ho raha hai
        except Exception:
            return await e.reply_text("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ.")

        if int(user_id) in VERIFIED_USERS or int(user_id) in SUDO_USERS:
            return await e.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴛʀᴀɪᴅ ᴛʜɪs ᴜsᴇʀ.")
            
        ACTIVE_TRAIDS[chat_id] = {
            "target_id": user_id, 
            "last_msg_id": None,
            "mention": user_mention
        }
        await e.reply_text(f"ᴛʀᴀɪᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! Ab aapke messages {user_mention} ko reply honge.", parse_mode=enums.ParseMode.HTML)
        
    elif cmd == "untraid":
        if chat_id in ACTIVE_TRAIDS:
            del ACTIVE_TRAIDS[chat_id]
            await e.reply_text("ᴛʀᴀɪᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ.")

@Client.on_message(filters.group, group=9)
async def target_message_tracker(xspam: Client, e: Message):
    chat_id = e.chat.id
    if chat_id in ACTIVE_TRAIDS:
        if e.from_user and e.from_user.id == ACTIVE_TRAIDS[chat_id]["target_id"]:
            ACTIVE_TRAIDS[chat_id]["last_msg_id"] = e.id

@Client.on_message((filters.me | filters.user(SUDO_USERS)) & filters.group, group=10)
async def traid_reply_handler(xspam: Client, e: Message):
    chat_id = e.chat.id
    
    if chat_id not in ACTIVE_TRAIDS:
        return
        
    text = e.text or e.caption
    if not text or text.startswith("."):
        return
        
    target_data = ACTIVE_TRAIDS[chat_id]
    target_msg_id = target_data["last_msg_id"]
    mention = target_data["mention"]
    
    # Pre-format the text to ALWAYS include the tag
    tagged_text = f"{text} {mention}"

    if not target_msg_id:
        try:
            await e.edit_text(tagged_text, parse_mode=enums.ParseMode.HTML)
        except Exception:
            pass
        return

    try:
        # Puraana code yahan sirf 'text' bhej raha tha, jiski wajah se tag nahi aata tha.
        # Ab hum 'tagged_text' bhej rahe hain.
        await xspam.send_message(
            chat_id, 
            tagged_text, 
            reply_to_message_id=target_msg_id,
            parse_mode=enums.ParseMode.HTML
        )
        await e.delete()
    except Exception as err:
        try:
            await e.edit_text(tagged_text, parse_mode=enums.ParseMode.HTML)
        except Exception:
            pass
            
