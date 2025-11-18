from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid.modules.basic.profile import extract_user
from Zaid.database import botbandb as BotDB

# MULTIPLE ADMINS
BOT_ADMINS = [8323081123, 7553434931]  # yaha apne ids daalo

@Client.on_message(filters.command("botban") & filters.user(BOT_ADMINS))
async def bot_ban_cmd(client: Client, message: Message):
    user = await extract_user(message)
    if not user:
        return await message.reply("User not found!")

    try:
        user = await client.get_users(user)
    except:
        return await message.reply("Invalid user!")

    if await BotDB.is_botbanned(user.id):
        return await message.reply("User already bot banned!")

    await BotDB.botban_user(user.id)
    await message.reply(
        f"🚫 **Bot-Banned:** [{user.first_name}](tg://user?id={user.id})"
    )


@Client.on_message(filters.command("botunban") & filters.user(BOT_ADMINS))
async def bot_unban_cmd(client: Client, message: Message):
    user = await extract_user(message)
    if not user:
        return await message.reply("User not found!")

    try:
        user = await client.get_users(user)
    except:
        return await message.reply("Invalid user!")

    if not await BotDB.is_botbanned(user.id):
        return await message.reply("User is not bot banned!")

    await BotDB.botunban_user(user.id)
    await message.reply(
        f"✅ **Bot-Unbanned:** [{user.first_name}](tg://user?id={user.id})"
    )
