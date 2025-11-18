from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid.database import botbandb as BotDB

BOT_ADMINS = [8323081123, 7553434931]

def get_target_user(message: Message):
    """username / user_id / reply se user laane ka simple method"""
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    
    if len(message.command) > 1:
        return message.command[1]  # username or ID
    
    return None


@Client.on_message(filters.command("botban") & filters.user(BOT_ADMINS))
async def bot_ban_cmd(client: Client, message: Message):

    target = get_target_user(message)
    if not target:
        return await message.reply("❌ User not found! Username ya reply do.")

    try:
        user = await client.get_users(target)
    except:
        return await message.reply("❌ Invalid user! Sahi username ya ID do.")

    if await BotDB.is_botbanned(user.id):
        return await message.reply("⚠️ User already bot-banned!")

    await BotDB.botban_user(user.id)
    await message.reply(
        f"🚫 **Bot-Banned:** [{user.first_name}](tg://user?id={user.id})"
    )



@Client.on_message(filters.command("botunban") & filters.user(BOT_ADMINS))
async def bot_unban_cmd(client: Client, message: Message):

    target = get_target_user(message)
    if not target:
        return await message.reply("❌ User not found! Username ya reply do.")

    try:
        user = await client.get_users(target)
    except:
        return await message.reply("❌ Invalid user! Sahi username ya ID do.")

    if not await BotDB.is_botbanned(user.id):
        return await message.reply("⚠️ User is NOT bot-banned!")

    await BotDB.botunban_user(user.id)
    await message.reply(
        f"✅ **Bot-Unbanned:** [{user.first_name}](tg://user?id={user.id})"
        )
