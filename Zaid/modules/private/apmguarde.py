from pyrogram import filters, Client
import asyncio
from Zaid import SUDO_USER
from Zaid.modules.help import *
from .pmguard import get_arg, denied_users

import Zaid.database.pmpermitdb as Zaid


# Database ko per-user support dena (har user ke liye alag key)
# Example: { user_id: { "pmguard": True/False, "permit_msg": "..." } }

@Client.on_message(filters.command("pmguard", ["."]) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand on or off**")
        return

    me = await client.get_me()
    user_id = me.id

    if arg == "off":
        await Zaid.set_pm(user_id, False)  # <- per-user flag
        await message.edit("**PM Guard Deactivated**")
    elif arg == "on":
        await Zaid.set_pm(user_id, True)   # <- per-user flag
        await message.edit("**PM Guard Activated**")


@Client.on_message(filters.command("setpmmsg", ["."]) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    me = await client.get_me()
    user_id = me.id

    if not arg:
        await message.edit("**What message to set**")
        return

    if arg == "default":
        await Zaid.set_permit_message(user_id, Zaid.PMPERMIT_MESSAGE)  # per-user
        await message.edit("**Anti_PM message set to default**.")
        return

    await Zaid.set_permit_message(user_id, f"`{arg}`")  # per-user
    await message.edit("**Custom anti-pm message set**")


add_command_help(
    "antipm",
    [
        [".pmguard [on or off]", " -> Activates or deactivates anti-pm (per-user)."],
        [".setpmmsg [message or default]", " -> Sets a custom anti-pm message."],
        [".setblockmsg [message or default]", "-> Sets custom block message."],
        [".setlimit [value]", " -> Sets a max. message limit for unwanted PMs and blocks when exceeded."],
        [".allow", " -> Allows a user to PM you."],
        [".deny", " -> Denies a user to PM you."],
    ],
)
