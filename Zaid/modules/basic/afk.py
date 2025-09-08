import asyncio
from datetime import datetime
import humanize
from pyrogram import filters, Client
from pyrogram.types import Message

from Zaid.helper.PyroHelpers import GetChatID, ReplyCheck
from Zaid.modules.help import add_command_help

# Global dictionary har user ke liye alag data
AFK_DATA = {}  # {user_id: {"afk": bool, "reason": str, "time": datetime, "users": {}, "groups": {}}}


def subtract_time(start, end):
    return humanize.naturaltime(start - end)


# Jab koi AFK bande ko mention kare ya DM kare
@Client.on_message(((filters.group & filters.mentioned) | filters.private) & ~filters.me & ~filters.service, group=3)
async def collect_afk_messages(bot: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None
    me = await bot.get_me()
    my_id = me.id

    if my_id not in AFK_DATA or not AFK_DATA[my_id]["afk"]:
        return

    last_seen = subtract_time(datetime.now(), AFK_DATA[my_id]["time"])
    is_group = message.chat.type in ["supergroup", "group"]
    CHAT_TYPE = AFK_DATA[my_id]["groups"] if is_group else AFK_DATA[my_id]["users"]

    if GetChatID(message) not in CHAT_TYPE:
        text = (
            f"**I'm AFK right now.**\n"
            f"⏱ Last seen: {last_seen}\n"
            f"📌 Reason: `{AFK_DATA[my_id]['reason']}`\n"
            f"Please wait until I come back."
        )
        await bot.send_message(
            chat_id=GetChatID(message),
            text=text,
            reply_to_message_id=ReplyCheck(message),
        )
        CHAT_TYPE[GetChatID(message)] = 1
    else:
        CHAT_TYPE[GetChatID(message)] += 1
        if CHAT_TYPE[GetChatID(message)] % 5 == 0:
            text = (
                f"**Still AFK...**\n"
                f"⏱ Last seen: {last_seen}\n"
                f"📌 Reason: `{AFK_DATA[my_id]['reason']}`"
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )


# AFK lagane ke liye (.afk <reason>)
@Client.on_message(filters.command("afk", ".") & filters.me, group=3)
async def afk_set(bot: Client, message: Message):
    me = await bot.get_me()
    my_id = me.id

    afk_text = " ".join(message.command[1:]) if len(message.command) > 1 else "No reason"
    AFK_DATA[my_id] = {
        "afk": True,
        "reason": afk_text,
        "time": datetime.now(),
        "users": {},
        "groups": {}
    }

    await message.edit(f"✅ You are now AFK.\n📌 Reason: `{afk_text}`")


# AFK hataane ke liye (!afk)
@Client.on_message(filters.command("afk", "!") & filters.me, group=3)
async def afk_unset(bot: Client, message: Message):
    me = await bot.get_me()
    my_id = me.id

    if my_id in AFK_DATA and AFK_DATA[my_id]["afk"]:
        last_seen = subtract_time(datetime.now(), AFK_DATA[my_id]["time"]).replace("ago", "").strip()
        await message.edit(
            f"👋 Welcome back!\n"
            f"⏱ You were AFK for {last_seen}.\n"
            f"💬 You got {sum(AFK_DATA[my_id]['users'].values()) + sum(AFK_DATA[my_id]['groups'].values())} messages from {len(AFK_DATA[my_id]['users']) + len(AFK_DATA[my_id]['groups'])} chats."
        )
        AFK_DATA[my_id] = {
            "afk": False,
            "reason": "",
            "time": None,
            "users": {},
            "groups": {}
        }
        await asyncio.sleep(5)


# Auto AFK unset jab tum khud message bhejo
@Client.on_message(filters.me & ~filters.service, group=3)
async def auto_afk_unset(bot: Client, message: Message):
    me = await bot.get_me()
    my_id = me.id

    if my_id in AFK_DATA and AFK_DATA[my_id]["afk"]:
        last_seen = subtract_time(datetime.now(), AFK_DATA[my_id]["time"]).replace("ago", "").strip()
        reply = await message.reply(
            f"👋 Welcome back!\n"
            f"⏱ You were AFK for {last_seen}.\n"
            f"💬 You got {sum(AFK_DATA[my_id]['users'].values()) + sum(AFK_DATA[my_id]['groups'].values())} messages from {len(AFK_DATA[my_id]['users']) + len(AFK_DATA[my_id]['groups'])} chats."
        )
        AFK_DATA[my_id] = {
            "afk": False,
            "reason": "",
            "time": None,
            "users": {},
            "groups": {}
        }
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
