import logging
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
from Zaid.database import botbandb as BotDB
from Zaid import app, API_ID, API_HASH
from pyrogram.types import CallbackQuery, InputMediaPhoto

user_sessions = {}
active_sessions = []

mongo_client = MongoClient(MONGO_URL)
db = mongo_client["SessionDB"]
sessions_col = db["UserSessions"] # Stores hosted sessions
users_col = db["AllBotUsers"]     # Stores all users who start the bot
# Button and message data
class Data:
    donate_button = [InlineKeyboardButton("⛈️ ᴅσηᴧᴛє ⛈️", callback_data="donate")]
    generate_single_button = [InlineKeyboardButton("⛈️ ʙᴀsɪᴄ ɢᴜɪᴅᴇ ⛈️", callback_data="guide")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")]
    ]

    back_buttons = [
        donate_button,
        [InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")]
    ]

    guide_buttons = [[InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")]]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("˹𝐏𝐫𝐨𝐱𝐲 ✘ 𝐇ᴏꜱᴛᴇʀ˼", url="https://t.me/Dark01Proxy_Bot")],
        [
            InlineKeyboardButton("❔ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ", callback_data="help"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ 🎶", callback_data="about")
        ],
        [
            InlineKeyboardButton("⚡ ᴜᴘᴅᴀᴛᴇ's", url="https://t.me/BMW_USERBOT_II"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ⛈️️", url="https://t.me/BMW_USERBOT_II")
        ],
        [InlineKeyboardButton("🌿 ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🌿", url="https://t.me/BMW0RACER")],
    ]

    START = """
**╭━━━〔 🌐 ɪɴғᴏ 🌐 〕━━━╮**
**┃ ✦ ʜᴇʟʟᴏ, ᴍʏ ɴᴀᴍᴇ ɪs : [˹𝐏𝐫𝐨𝐱𝐲 ✘ 𝐇ᴏꜱᴛᴇʀ˼](https://t.me/Dark01Proxy_Bot)**  
**┃ ✦ ᴘʟᴇᴀsᴜʀᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !**  
**╰━━━━━━━━━━━━━━━━━━╯**

**➤ ᴀ sᴛʀᴏɴɢ & ᴜsᴇғᴜʟ ɪᴅ-ʙᴏᴛ**  
**➤ ғᴜɴ ғᴇᴀᴛᴜʀᴇs ᴀʀᴇ ᴀᴠᴀɪʟᴀʙʟᴇ**  
**➤ ʜᴇʟᴘs ʏᴏᴜ ᴘᴏᴡᴇʀ ᴜᴘ ʏᴏᴜʀ ɪᴅ**  

**⟡──────────────⟡**  
**➤ ᴄʀᴇᴀᴛᴇᴅ ʙʏ : [꧁𓊈𒆜🆃🅷🅴 🅱🅼🆆𒆜𓊉꧂](https://t.me/BMW0RACER) 🚩**  
**⟡──────────────⟡**
"""

    HELP = """
**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ** ⚡

**/start - ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ**
/help - ᴏᴘᴇɴ ʜᴇʟᴘ ᴍᴇɴᴜ**
/about - ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴏᴡɴᴇʀ**
**/add - ᴀᴜᴛᴏ-ʜᴏsᴛ ᴛʜᴇ ʙᴏᴛ**
**/clone - ᴄʟᴏɴᴇ ᴠɪᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ**
**/remove - ʟᴏɢᴏᴜᴛ ғʀᴏᴍ ʙᴏᴛ**
"""

    GUIDE = """**❖ ʜᴇʏ ᴅᴇᴀʀ, ᴛʜɪs ɪs ᴀ ǫᴜɪᴄᴋ ᴀɴᴅ sɪᴍᴘʟᴇ ɢᴜɪᴅᴇ ᴛᴏ ʜᴏsᴛɪɴɢ [ᴜsᴇʀʙᴏᴛ](https://t.me/BMW_USER_01_BOT)**

**1) Sᴇɴᴅ /add ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴛʜᴇ ʙᴏᴛ **
**2) Sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (ᴇ.ɢ. +917800000000)**  
**3) ᴄʜᴇᴄᴋ ʏᴏᴜʀ ɪᴅ ᴘᴇʀsᴏɴᴀʟ ᴍᴀssᴀɢᴇ ғᴏʀᴍ ᴛᴇʟᴇɢʀᴀᴍ, ᴀɴᴅ ᴄᴏᴘʏ ᴏʀ ʀᴇᴍɪɴᴅ ᴏᴛᴘ ᴀɴᴅ sᴇɴᴅ ᴛʜɪs ʙᴏᴛ sᴘᴀᴄᴇ ʙʏ sᴘᴀᴄᴇ ʟɪᴋᴇ :- 1 2 3 4 5**

**➤ ɪғ ʏᴏᴜ sᴇᴛ ᴛᴡᴏ sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴄᴏᴅᴇ ᴏɴ ʏᴏᴜʀ ɪᴅ , ᴛʜᴇɴ sᴇɴᴅ ᴛʜᴀᴛ ᴄᴏᴅᴇ.**
**➤ ʏᴏᴜʀ ʙᴏᴛ ᴡɪʟʟ ʙᴇ ʜᴏsᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟ.**

**ɪғ ʏᴏᴜ sᴛɪʟʟ ғᴀᴄᴇ ᴀɴʏ ɪssᴜᴇs, ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ʀᴇᴀᴄʜ ᴏᴜᴛ ғᴏʀ sᴜᴘᴘᴏʀᴛ.**"""

    ABOUT = """
**ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ** 🌙

**ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴛᴏ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ ᴡɪᴛʜ ʙᴇᴀᴜᴛɪғᴜʟ ᴀɴɪᴍᴀᴛɪᴏɴ.**

**sᴜᴘᴘᴏʀᴛᴇᴅ :- ʀᴇᴘʟʏ-ʀᴀɪᴅ, ɪᴅ-ᴄʟᴏɴᴇ, ʀᴀɪᴅ, sᴘᴀᴍ, ᴜsᴇʀ-ᴛᴀɢɢᴇʀ ᴇᴛᴄ.**

**◌ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ](https://www.python.org)**
**◌ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [꧁𓊈𒆜🆃🅷🅴 🅱🅼🆆𒆜𓊉꧂](https://t.me/BMW0RACER)**
**◌ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [꧁𓊈𒆜🆃🅷🅴 🅱🅼🆆𒆜𓊉꧂](https://t.me/BMW0RACER)**
"""

    DONATE = """
**❖ ʜᴇʏ, ɪ ᴀᴍ ɢʟᴀᴅ ᴛᴏ ᴋɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ ᴅᴏɴᴀᴛɪɴɢ ᴜs ᴛʜᴀᴛ ᴍᴇᴀɴ ᴀ ʟᴏᴛ :)**

**ᴡᴇ ᴘʀᴏᴠɪᴅᴇ 24×7 ᴜsᴇʙᴏᴛ ʜᴏsᴛɪɴɢ sᴇʀᴠɪᴄᴇ. sᴏ ᴡᴇ ᴀʟsᴏ ɴᴇᴇᴅ sᴏᴍᴇ ʜᴇʟᴘ ғᴏʀ ɪᴛ, ᴅᴏɴᴀᴛᴇ ɴᴏᴡ ᴠɪᴀ :-**
**• ᴜᴘɪ ɪᴅ » **`himanshu49@fam or himanshu4hk9@okhdfcbank`
**• ǫʀ ᴄᴏᴅᴇ » [ᴛᴀᴘ ᴛᴏ sᴇᴇ ǫʀ ᴄᴏᴅᴇ](https://t.me/GOJO_PAY_49) **
**• ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ʙʏ ᴄᴏɴᴛᴀᴄᴛɪɴɢ [ᴅᴇᴠᴇʟᴏᴘᴇʀ](https://t.me/BMW0RACER) 🚩**

**ʏᴏᴜʀ sᴍᴀʟʟ ᴀᴍᴏᴜɴᴛ ᴄᴀɴ ʜᴇʟᴘ ᴜs ᴀɴᴅ sᴛʀᴀɴɢᴇʀ ᴛᴏ ɢʀᴏᴡ ᴍᴏʀᴇ**
"""

# Command
@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):

    # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )

    # 🔥 NORMAL START MESSAGE
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=InlineKeyboardMarkup(Data.buttons)
    )





@app.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):

        # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )
    
    await message.reply_text(
        Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

@app.on_message(filters.command("about") & filters.private)
async def about_command(client: Client, message: Message):

        # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )
    
    await message.reply_text(
        Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# --- SUDO COMMANDS: STATS & BROADCAST ---

@app.on_message(filters.command("stats") & filters.user(8283497747))
async def stats_handler(client: Client, message: Message):
    users_count = users_col.count_documents({})
    hosted_count = sessions_col.count_documents({})
    
    msg_text = (
        "**📊 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs**\n\n"
        f"**👤 ᴛᴏᴛᴀʟ ᴜsᴇʀs:** `{users_count}`\n"
        f"**🔌 ʜᴏsᴛᴇᴅ sᴇssɪᴏɴs:** `{hosted_count}`\n"
        "**⚙️ ᴠᴇʀsɪᴏɴ:** `v3.0`\n"
        f"**✅ sᴛᴀᴛᴜs:** `Alive & Running`"
    )
    await message.reply(msg_text)

@app.on_message(filters.command("broadcast") & filters.user(8283497747))
async def broadcast_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("❌ **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.**")

    to_send = message.reply_to_message
    users = users_col.find({})
    total_users = users_col.count_documents({})
    
    success = 0
    failed = 0
    blocked = 0
    deactivated = 0
    
    status_msg = await message.reply(f"**⏳ ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ ᴛᴏ {total_users} ᴜsᴇʀs...**")
    
    for user in users:
        user_id = user["_id"]
        try:
            await to_send.copy(chat_id=user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await to_send.copy(chat_id=user_id)
            success += 1
        except UserIsBlocked:
            blocked += 1
            # Optional: Delete user from DB if blocked
            # users_col.delete_one({"_id": user_id}) 
        except InputUserDeactivated:
            deactivated += 1
            users_col.delete_one({"_id": user_id})
        except Exception:
            failed += 1
            
    await status_msg.edit(
        "**✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**\n\n"
        f"**📬 sᴇɴᴛ:** `{success}`\n"
        f"**🚫 ʙʟᴏᴄᴋᴇᴅ:** `{blocked}`\n"
        f"**💀 ᴅᴇʟᴇᴛᴇᴅ:** `{deactivated}`\n"
        f"**❌ ғᴀɪʟᴇᴅ:** `{failed}`"
    )


# Callback queries
@app.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "home":
        await query.message.edit_media(
            media=InputMediaPhoto(ALIVE_PIC, caption=Data.START),
            reply_markup=InlineKeyboardMarkup(Data.buttons)
        )
    elif data == "help":
        await query.message.edit_text(
            Data.HELP,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    elif data == "about":
        await query.message.edit_text(
            Data.ABOUT,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    elif data == "donate":
        await query.message.edit_text(
            Data.DONATE,
            reply_markup=InlineKeyboardMarkup(Data.guide_buttons)
        )
    elif data == "guide":
        await query.message.edit_text(
            Data.GUIDE,
            reply_markup=InlineKeyboardMarkup(Data.back_buttons)
        )

async def restart_all_sessions():
    logging.info("ʀᴇsᴛᴀʀᴛɪɴɢ ᴀʟʟ ᴜsᴇʀ's ᴀᴄᴛɪᴠᴇ sᴇssɪᴏɴs...")
    sessions = sessions_col.find()
    for session in sessions:
        try:
            uid = session["user_id"]
            string = session["session"]
            client = Client(
                name=f"AutoClone_{uid}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string,
                plugins=dict(root="Zaid/modules")
            )
            await client.start()
            active_sessions.append(client)
            logging.info(f"sᴛᴀʀᴛᴇᴅ sᴇssɪᴏɴ ғᴏʀ ᴜsᴇʀ {uid}")
        except Exception as e:
            logging.error(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴛᴀʀᴛ sᴇssɪᴏɴ ғᴏʀ ᴜsᴇʀ {uid}: {e}")

@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message: Message):

        # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )
    
    reply_markup = InlineKeyboardMarkup(Data.buttons)
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=reply_markup)

@app.on_message(filters.command("clone") & filters.private)
async def clone(bot: app, msg: Message):

        # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )
   
    chat = msg.chat
    text = await msg.reply("❍ FIRST GEN SESSION \n\n𔓕 /clone session\n\n❍ OR - USE  \n\n𔓕 /add ( ғᴏʀ ᴀᴜᴛᴏ-ʜᴏsᴛ )")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
        
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=phone, plugins=dict(root="Zaid/modules"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f"❖ ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ʀᴇᴀᴅʏ ᴛᴏ ғɪɢʜᴛ\n\n❍ ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ\n\n❖ {user.first_name}")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\n ᴘʀᴇss /start ᴛᴏ sᴛᴀʀᴛ ᴀɢᴀɪɴ.")


@app.on_message(filters.command("add") & filters.private)
async def add_session_command(client, message: Message):

        # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )

    user_id = message.from_user.id
    await message.reply("📲 ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (e.g., +918200000009):")
    user_sessions[user_id] = {"step": "awaiting_phone"}


@app.on_message(filters.command("remove") & filters.private)
async def remove_session(_, msg: Message):

        # 🔥 BOT BAN CHECK
    if await BotDB.is_botbanned(message.from_user.id):
        return await client.send_message(
            chat_id=message.chat.id,
            text=(
                "**🚫 You Are Banned From Using This Bot!**\n"
                "Baap ke DM jaa kar @BMW0RACER **sorry bol** 😈\n\n"
                "You cannot access the bot commands."
            )
        )
    
    uid = msg.from_user.id
    session_data = sessions_col.find_one({"_id": uid})
    if not session_data:
        return await msg.reply("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ sᴇssɪᴏɴ ғᴏᴜɴᴅ.")

    try:
        for client in active_sessions:
            if client.name == f"AutoClone_{uid}":
                await client.stop()
                active_sessions.remove(client)
                break
        sessions_col.delete_one({"_id": uid})
        await msg.reply("✅ ʏᴏᴜʀ sᴇssɪᴏɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
    except Exception as e:
        await msg.reply(f"⚠️ ᴇʀʀᴏʀ ᴛᴏ ʀᴇᴍᴏᴠɪɴɢ sᴇssɪᴏɴ:\n`{e}`")

@app.on_message()
async def session_handler(_, msg: Message):
    uid = msg.from_user.id
    session = user_sessions.get(uid)
    if not session:
        return

    step = session.get("step")
    if step == "awaiting_phone":
        phone = msg.text.strip()
        client = Client(name=f"gen_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        session.update({"phone": phone, "client": client})
        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply("📨 OTP sᴇɴᴛ! ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴛʜɪs ғᴏʀᴍᴀᴛ: `1 2 3 4 5` ( sᴘᴀᴄᴇ ʙʏ sᴘᴀᴄᴇ )")
        except Exception as e:
            await msg.reply(f"❌ ᴏᴛᴘ ᴡᴀs ᴡʀᴏɴɢ ᴏʀ ᴇxᴘɪʀᴇᴅ :\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        otp = msg.text.strip()
        client = session["client"]
        try:
            await client.sign_in(phone_number=session["phone"], phone_code_hash=session["phone_code_hash"], phone_code=otp)
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            return await msg.reply("🔐 sᴇɴᴅ ʏᴏᴜʀ 2FA ᴘᴀssᴡᴏʀᴅ.")
        except Exception as e:
            await msg.reply(f"❌ ʏᴏᴜʀ 2FA ᴘᴀssᴡᴏʀᴅ ᴡʀᴏɴɢ ғᴀɪʟᴇᴅ ᴛᴏ sɪɢɴ ɪɴ:\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return
        await finalize_login(client, msg, uid)

    elif step == "awaiting_2fa":
        password = msg.text.strip()
        client = session["client"]
        try:
            await client.check_password(password)
            await finalize_login(client, msg, uid)
        except Exception as e:
            await msg.reply(f"❌ ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ:\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

async def finalize_login(client: Client, msg: Message, uid: int):
    try:
        string = await client.export_session_string()
        user = await client.get_me()

        sessions_col.update_one(
            {"_id": uid},
            {"$set": {
                "session": string,
                "name": user.first_name,
                "user_id": user.id,
                "username": user.username
            }},
            upsert=True
        )

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await hosted.start()
        active_sessions.append(hosted)

        await msg.reply(f"✅ ʟᴏɢɢᴇᴅ ɪɴ ᴀs **{user.first_name}**.\n\n🔐 sᴇssɪᴏɴ sᴛʀɪɴɢ:\n\n`{string}`\n\nᴀᴜᴛᴏ-ʜᴏsᴛ ɴᴏᴡ..\n\n|| 🔪ᴛᴏ ʙᴏᴛ ғʀᴏᴍ ʏᴏᴜʀ ɪᴅ sᴇɴᴅ ᴛʜɪs ᴄᴍᴅ  /remove .... ||")
    except Exception as e:
        await msg.reply(f"❌ ғɪɴᴀʟ sᴛᴇᴘ ғᴀɪʟᴇᴅ \nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴜsᴇ ᴄᴍᴅ /add \n`{e}`")
    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)
