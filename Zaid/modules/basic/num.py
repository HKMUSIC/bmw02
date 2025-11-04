import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from Zaid.modules.help import add_command_help

# Special users who can use the commands
OWNER_IDS = [7659846392, 8278874316, 5134011952, 8362207412, 6455955034]   # add more user IDs if needed
GROUP_ID = -1002977931385
BOT_USERNAME = "@IntelXGroupV4Bot"


def is_authorized(user_id: int) -> bool:
    return user_id in OWNER_IDS


async def fetch_bot_reply(client: Client, query: str, command: str) -> str:
    """
    Sends a command into the group and waits for a bot reply.
    Returns the text wrapped with triple backticks and footer.
    """
    # Send request into group
    await client.send_message(GROUP_ID, f"/{command} {query}")

    # Wait for bot response
    await asyncio.sleep(8)

    async for msg in client.get_chat_history(GROUP_ID, limit=30):
        if not msg.from_user or not getattr(msg.from_user, "is_bot", False):
            continue

        username = (msg.from_user.username or "").lower()
        if username != BOT_USERNAME.lower():
            continue

        content = msg.text if msg.text else (msg.caption or "")
        if not content:
            continue

        if query not in content:
            continue

        # Wrap text with triple backticks + footer
        wrapped = f"```\n{content.strip()}\n```"
        wrapped += "\n<pre>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - 𝛅 ⴕ ᧘ ᥧ 𝚱 𝛜 Ʀ ⌯</pre>"
        return wrapped

    return None


# ========================= .stkr =========================
@Client.on_message(filters.command(["stkr"], ".") & filters.me)
async def stkr(client: Client, message: Message):
    if message.from_user and not is_authorized(message.from_user.id):
        return await message.edit_text(
            "❌ ʙᴀʙʏ ᴏɴʟʏ ᴘᴀɪᴅ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.\nᴅᴍ @hehe_stalker ғᴏʀ ᴘᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴀᴄᴄᴇss!"
        )

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit() or len(args[1]) != 10:
        return await message.edit_text(
            "❌ Please provide a valid 10-digit number.\nExample: `.stkr 1234567890`"
        )

    number = args[1]
    status = await message.edit_text(f"🔎 Fetching details for `{number}` ...")

    final_text = await fetch_bot_reply(client, number, "num")

    if not final_text:
        return await status.edit_text(
            "📞 Mobile Info Result:\n```\nmessage- No matching records found\n```\n"
            "<pre>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - 𝛅 ⴕ ᧘ ᥧ 𝚱 𝛜 Ʀ ⌯</pre>"
        )

    await client.send_message(message.chat.id, final_text)
    await status.delete()


# ========================= .adhar =========================
@Client.on_message(filters.command(["adhar"], ".") & filters.me)
async def adhar(client: Client, message: Message):
    if message.from_user and not is_authorized(message.from_user.id):
        return await message.edit_text(
            "❌ ʙᴀʙʏ ᴏɴʟʏ ᴘᴀɪᴅ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.\nᴅᴍ @hehe_stalker ғᴏʀ ᴘᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴀᴄᴄᴇss!"
        )

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit() or len(args[1]) != 12:
        return await message.edit_text(
            "❌ Please provide a valid 12-digit number.\nExample: `.adhar 123412341234`"
        )

    number = args[1]
    status = await message.edit_text(f"🔎 Fetching Aadhaar details for `{number}` ...")

    final_text = await fetch_bot_reply(client, number, "aadhar")

    if not final_text:
        return await status.edit_text(
            "📞 Mobile Info Result:\n```\nmessage- No matching records found\n```\n"
            "<pre>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - 𝛅 ⴕ ᧘ ᥧ 𝚱 𝛜 Ʀ ⌯</pre>"
        )

    await client.send_message(message.chat.id, final_text)
    await status.delete()


# ========================= .upiinfo =========================
@Client.on_message(filters.command(["upiinfo"], ".") & filters.me)
async def upiinfo(client: Client, message: Message):
    if message.from_user and not is_authorized(message.from_user.id):
        return await message.edit_text(
            "❌ ʙᴀʙʏ ᴏɴʟʏ ᴘᴀɪᴅ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.\nᴅᴍ @hehe_stalker ғᴏʀ ᴘᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴀᴄᴄᴇss!"
        )

    args = message.text.split()
    if len(args) != 2 or "@" not in args[1]:
        return await message.edit_text(
            "❌ Please provide a valid UPI ID.\nExample: `.upiinfo example@upi`"
        )

    upi_id = args[1]
    status = await message.edit_text(f"🔎 Fetching UPI Info for `{upi_id}` ...")

    final_text = await fetch_bot_reply(client, upi_id, "upiinfo")

    if not final_text:
        return await status.edit_text(
            "📞 UPI Info Result:\n```\nmessage- No matching records found\n```\n"
            "<pre>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - 𝛅 ⴕ ᧘ ᥧ 𝚱 𝛜 Ʀ ⌯</pre>"
        )

    await client.send_message(message.chat.id, final_text)
    await status.delete()


# ========================= .upinum =========================
@Client.on_message(filters.command(["upinum"], ".") & filters.me)
async def upinum(client: Client, message: Message):
    if message.from_user and not is_authorized(message.from_user.id):
        return await message.edit_text(
            "❌ ʙᴀʙʏ ᴏɴʟʏ ᴘᴀɪᴅ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.\nᴅᴍ @hehe_stalker ғᴏʀ ᴘᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴀᴄᴄᴇss!"
        )

    args = message.text.split()
    if len(args) != 2 or "@" not in args[1]:
        return await message.edit_text(
            "❌ Please provide a valid UPI ID.\nExample: `.upinum example@upi`"
        )

    upi_id = args[1]
    status = await message.edit_text(f"🔎 Fetching UPI Number details for `{upi_id}` ...")

    final_text = await fetch_bot_reply(client, upi_id, "upinum")

    if not final_text:
        return await status.edit_text(
            "📞 UPI Number Result:\n```\nmessage- No matching records found\n```\n"
            "<pre>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - 𝛅 ⴕ ᧘ ᥧ 𝚱 𝛜 Ʀ ⌯</pre>"
        )

    await client.send_message(message.chat.id, final_text)
    await status.delete()


# ========================= Add Help =========================
add_command_help(
    "stkr",
    [
        [
            "stkr <10digit>",
            "Fetches number info from your private group bot. Reply is copied, wrapped in triple backticks, and footer is added.",
        ],
    ],
)

add_command_help(
    "adhar",
    [
        [
            "adhar <12digit>",
            "Fetches Aadhaar info from your private group bot. Reply is copied, wrapped in triple backticks, and footer is added.",
        ],
    ],
)

add_command_help(
    "upiinfo",
    [
        [
            "upiinfo <upi_id>",
            "Fetches UPI info from your private group bot. Reply is copied, wrapped in triple backticks, and footer is added.",
        ],
    ],
)

add_command_help(
    "upinum",
    [
        [
            "upinum <upi_id>",
            "Fetches UPI number details from your private group bot. Reply is copied, wrapped in triple backticks, and footer is added.",
        ],
    ],
          )
      
