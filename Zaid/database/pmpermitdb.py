from Zaid.database import cli

collection = cli["Zaid"]["pmpermit"]

PMPERMIT_MESSAGE = (
    "**ᴡᴀʀɴɪɴɢ!⚠️ ᴘʟᴢ ʀᴇᴀᴅ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴄᴀʀᴇꜰᴜʟʟʏ..\n\n**"
    "**ɪ'ᴍ ʙᴍᴡ ᴜꜱᴇʀʙᴏᴛ ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ᴍʏ ᴍᴀꜱᴛᴇʀ ꜰʀᴏᴍ ꜱᴘᴀᴍᴍᴇʀꜱ.**"
    "**ɪꜰ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ꜱᴘᴀᴍᴍᴇʀ ᴛʜᴇɴ ᴘʟᴢ ᴡᴀɪᴛ!.\n\n**"
    "**ᴜɴᴛɪʟ ᴛʜᴇɴ, ᴅᴏɴ'ᴛ ꜱᴘᴀᴍ, ᴏʀ ʏᴏᴜ'ʟʟ ɢᴇᴛ ʙʟᴏᴄᴋᴇᴅ ᴀɴᴅ ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ ᴍᴇ, ꜱᴏ ʙᴇ ᴄᴀʀᴇꜰᴜʟʟ ᴛᴏ ꜱᴇɴᴅ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇꜱ!**"
)

BLOCKED = "**ʙᴇᴇᴘ ʙᴏᴏᴘ ꜰᴏᴜɴᴅᴇᴅ ᴀ ꜱᴘᴀᴍᴍᴇʀ!, ʙʟᴏᴄᴋᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**"

LIMIT = 5


# ------------------- PER USER FUNCTIONS -------------------

async def set_pm(user_id: int, value: bool):
    await collection.update_one(
        {"_id": user_id},
        {"$set": {"pmpermit": value}},
        upsert=True,
    )


async def get_pm(user_id: int):
    result = await collection.find_one({"_id": user_id})
    if not result:
        return False
    return result.get("pmpermit", False)


async def set_permit_message(user_id: int, text: str):
    await collection.update_one(
        {"_id": user_id},
        {"$set": {"pmpermit_message": text}},
        upsert=True,
    )


async def get_permit_message(user_id: int):
    result = await collection.find_one({"_id": user_id})
    if not result:
        return PMPERMIT_MESSAGE
    return result.get("pmpermit_message", PMPERMIT_MESSAGE)


async def set_block_message(user_id: int, text: str):
    await collection.update_one(
        {"_id": user_id},
        {"$set": {"block_message": text}},
        upsert=True,
    )


async def get_block_message(user_id: int):
    result = await collection.find_one({"_id": user_id})
    if not result:
        return BLOCKED
    return result.get("block_message", BLOCKED)


async def set_limit(user_id: int, limit: int):
    await collection.update_one(
        {"_id": user_id},
        {"$set": {"limit": limit}},
        upsert=True,
    )


async def get_limit(user_id: int):
    result = await collection.find_one({"_id": user_id})
    if not result:
        return LIMIT
    return result.get("limit", LIMIT)


# ------------------- APPROVED USERS (PER USER) -------------------

async def allow_user(user_id: int, chat: int):
    await collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"approved_users": chat}},
        upsert=True,
    )


async def get_approved_users(user_id: int):
    result = await collection.find_one({"_id": user_id})
    if result:
        return result.get("approved_users", [])
    return []


async def deny_user(user_id: int, chat: int):
    await collection.update_one(
        {"_id": user_id},
        {"$pull": {"approved_users": chat}},
        upsert=True,
    )
