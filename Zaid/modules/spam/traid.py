import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Importing required variables from your bot's database
from cache.data import *
from Zaid.database.rraid import *
from Zaid import SUDO_USER

SUDO_USERS = SUDO_USER

# List ki jagah dictionary use kar rahe hain taaki group wise target save ho sake
ACTIVE_TRAIDS = {}

@Client.on_message(
    filters.command(["traid", "untraid"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def traid_cmd(xspam: Client, e: Message):
    cmd = e.command[0]
    chat_id = e.chat.id
    
    if cmd == "traid":
        args = e.text.split(maxsplit=1)
        target_user = None
        
        # Agar message ko reply kiya hai
        if e.reply_to_message:
            target_user = e.reply_to_message.from_user.id
        # Agar command ke aage @username ya userid diya hai
        elif len(args) > 1:
            target_user = args[1]
        else:
            return await e.reply_text("ᴜsᴀɢᴇ: `.ᴛʀᴀɪᴅ @ᴜsᴇʀɴᴀᴍᴇ` / `ᴜsᴇʀɪᴅ` ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ.\nᴛᴏ sᴛᴏᴘ: `.ᴜɴᴛʀᴀɪᴅ`")
            
        try:
            # Pyrogram khud username ya id se user ki details nikal lega
            user = await xspam.get_users(target_user)
            user_id = user.id
            first_name = user.first_name
        except Exception:
            return await e.reply_text("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ ᴏʀ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")

        # VERIFIED_USERS list database / data se aani chahiye
        if int(user_id) in VERIFIED_USERS:
            return await e.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴛʀᴀɪᴅ ᴠᴇʀɪғɪᴇᴅ ᴜsᴇʀs 😈")
        elif int(user_id) in SUDO_USERS:
            return await e.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴛʀᴀɪᴅ sᴜᴅᴏ ᴜsᴇʀs 🛡️")
            
        # Chat ID ke hisaab se target save kar rahe hain
        ACTIVE_TRAIDS[chat_id] = {"id": user_id, "name": first_name}
        await e.reply_text(f"ᴛʀᴀɪᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴏɴ {first_name} 😈\n(ᴀʙ ᴀᴀᴘ ᴊᴏ ʙʜɪ ᴛʏᴘᴇ ᴋᴀʀᴇɴɢᴇ, ʏᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴛᴀɢ ʜᴏ ᴊᴀʏᴇɢᴀ)")
        
    elif cmd == "untraid":
        if chat_id in ACTIVE_TRAIDS:
            target_name = ACTIVE_TRAIDS[chat_id]["name"]
            del ACTIVE_TRAIDS[chat_id]
            await e.reply_text(f"ᴛʀᴀɪᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ {target_name} 🤫")
        else:
            await e.reply_text("ᴛʀᴀɪᴅ ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")

# Watcher ab aapke aur SUDO users ke messages sune ga
@Client.on_message((filters.me | filters.user(SUDO_USERS)) & filters.group, group=10)
async def traid_watcher(xspam: Client, e: Message):
    chat_id = e.chat.id
    
    # Agar is group me koi traid active nahi hai, toh ignore karo
    if chat_id not in ACTIVE_TRAIDS:
        return
        
    # Userbot commands ko tag nahi karna hai (jaise .ping, .help)
    if e.text and e.text.startswith("."):
        return
        
    target = ACTIVE_TRAIDS[chat_id]
    target_id = target["id"]
    target_name = target["name"]
    
    # Target ka invisible ya normal mention banayenge
    mention = f"[{target_name}](tg://user?id={target_id})"
    
    # Sirf text messages pe kaam karega taaki photos/stickers kharab na ho
    if e.text:
        # Agar message aapne khud (filters.me) bheja hai
        if e.from_user and e.from_user.is_self:
            try:
                # Ye aapke message ko edit karke aage tag add kar dega
                await e.edit_text(f"{e.text} {mention}")
            except Exception:
                pass
        # Agar message kisi aur SUDO user ne bheja hai (Sudo ki msg bot edit nahi kar sakta)
        else:
            try:
                await e.reply_text(mention)
            except Exception:
                pass
                
