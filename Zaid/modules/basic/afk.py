import asyncio
from datetime import datetime
import humanize
from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid.helper.PyroHelpers import GetChatID, ReplyCheck
from Zaid.modules.help import add_command_help

# Global Vars
AFK = False
AFK_REASON = ""
AFK_TIME = None
USERS = {}
GROUPS = {}

def subtract_time(start, end):
    return humanize.naturaltime(start - end)

# Jab koi AFK bande ko mention kare ya DM kare
@Client.on_message(((filters.group & filters.mentioned) | filters.private) & ~filters.me & ~filters.service, group=3)
async def collect_afk_messages(bot: Client, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME)
        is_group = message.chat.type in ["supergroup", "group"]
        CHAT_TYPE = GROUPS if is_group else USERS

        if GetChatID(message) not in CHAT_TYPE:
            text = (
                f"**I'm AFK right now.**\n"
                f"⏱ Last seen: {last_seen}\n"
                f"📌 Reason: `{AFK_REASON}`\n"
                f"Please wait until I come back."
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )
            CHAT_TYPE[GetChatID(message)] = 1
            return
        else:
            # Spam control
            CHAT_TYPE[GetChatID(message)] += 1
            if CHAT_TYPE[GetChatID(message)] % 5 == 0:
                text = (
                    f"**Still AFK...**\n"
                    f"⏱ Last seen: {last_seen}\n"
                    f"📌 Reason: `{AFK_REASON}`"
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                )

# AFK lagane ke liye (.afk <reason>)
@Client.on_message(filters.command("afk", ".") & filters.me, group=3)
async def afk_set(bot: Client, message: Message):
    global AFK, AFK_REASON, AFK_TIME
    afk_text = " ".join(message.command[1:]) if len(message.command) > 1 else "No reason"
    AFK = True
    AFK_REASON = afk_text
    AFK_TIME = datetime.now()

    await message.edit(f"✅ You are now AFK.\n📌 Reason: `{AFK_REASON}`")

# AFK hataane ke liye (!afk)
@Client.on_message(filters.command("afk", "!") & filters.me, group=3)
async def afk_unset(bot: Client, message: Message):
    global AFK, AFK_REASON, AFK_TIME, USERS, GROUPS
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        await message.edit(
            f"👋 Welcome back!\n"
            f"⏱ You were AFK for {last_seen}.\n"
            f"💬 You got {sum(USERS.values()) + sum(GROUPS.values())} messages from {len(USERS) + len(GROUPS)} chats."
        )
        AFK = False
        AFK_REASON = ""
        AFK_TIME = None
        USERS, GROUPS = {}, {}
        await asyncio.sleep(5)

# Auto AFK unset jab tum khud message bhejo
@Client.on_message(filters.me & ~filters.service, group=3)
async def auto_afk_unset(bot: Client, message: Message):
    global AFK, AFK_REASON, AFK_TIME, USERS, GROUPS
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        reply = await message.reply(
            f"👋 Welcome back!\n"
            f"⏱ You were AFK for {last_seen}.\n"
            f"💬 You got {sum(USERS.values()) + sum(GROUPS.values())} messages from {len(USERS) + len(GROUPS)} chats."
        )
        AFK = False
        AFK_REASON = ""
        AFK_TIME = None
        USERS, GROUPS = {}, {}
        await asyncio.sleep(5)
        await reply.delete()

add_command_help(
    "afk",
    [
        [".afk <reason>", "Set yourself AFK with an optional reason."],
        ["!afk", "Manually turn off AFK."],
        ["Auto remove", "AFK will auto remove when you send any message."],
    ],
            )
