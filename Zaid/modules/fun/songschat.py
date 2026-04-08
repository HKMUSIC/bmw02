import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Temporary database songs store karne ke liye.
# (Note: Agar aap userbot restart karoge toh ye clear ho jayega. 
# Parmanent save ke liye aage chal kar database add kiya ja sakta hai.)
SONGS_DB = {}


@Client.on_message(filters.command(["addsong"], ["/", "."]) & filters.me)
async def save_song(client: Client, message: Message):
    """
    Kise lyrics wale message ko reply karke time(delay) specify karo.
    Example: .addsong 2
    """
    if not message.reply_to_message or not message.reply_to_message.text:
        await message.edit("`Bhai, pehle kisi lyrics wale text message ko reply kar.`\n**Format:** `.addsong <delay_in_seconds>`")
        return

    cmd = message.command
    if len(cmd) < 2:
        await message.edit("`Time (delay) mention karna bhool gaya bhai!`\n**Format:** `.addsong 2`")
        return

    try:
        delay = float(cmd[1])
    except ValueError:
        await message.edit("`Delay numbers me hona chahiye (e.g., 2 or 1.5).`")
        return

    # Reply kiye gaye message se lines nikalna
    lyrics = message.reply_to_message.text
    # Khaali lines ko ignore karke list banayenge
    lines = [line.strip() for line in lyrics.split("\n") if line.strip()]

    if len(lines) < 2:
        await message.edit("`Song me kam se kam 2 lines toh honi chahiye na!`")
        return

    # First line humara "Trigger" banegi (usko lowercase karke save karenge taaki case-sensitive na rahe)
    trigger_key = lines[0].lower()
    original_first_line = lines[0]
    rest_of_the_lines = lines[1:]

    # Database me save karna
    SONGS_DB[trigger_key] = {
        "first_line": original_first_line,
        "lines": rest_of_the_lines,
        "delay": delay
    }

    await message.edit(
        f"✅ **Song Saved Successfully!**\n\n"
        f"⏱ **Delay:** `{delay}s`\n"
        f"🔑 **Trigger (First Line):** `{original_first_line}`\n\n"
        f"Jab bhi tu chat me exact **{original_first_line}** likhega, bot baaki lines automatically bhej dega."
    )


# --- FEATURE 1: AUTO TRIGGER ON FIRST LINE ---
@Client.on_message(filters.text & filters.me, group=1)
async def auto_play_song(client: Client, message: Message):
    text_lower = message.text.strip().lower()

    # Commands ko ignore karega taaki clash na ho
    if text_lower.startswith((".", "/")):
        return

    if text_lower in SONGS_DB:
        song_data = SONGS_DB[text_lower]
        delay = song_data["delay"]
        lines = song_data["lines"]

        for line in lines:
            await asyncio.sleep(delay)
            await client.send_message(message.chat.id, line)


# --- FEATURE 2: TAGGING WITH .SONG COMMAND ---
@Client.on_message(filters.command("song", ".") & filters.me)
async def target_song(client: Client, message: Message):
    """
    Format: .song <first line> @username
    Ye specific user ko tag karke poora song bheja karega.
    """
    cmd = message.command
    if len(cmd) < 3:
        await message.edit("`Format: .song <first_line> @username`\n`Example: .song oh ho ho ho @zaid`")
        return

    # Last argument ko username aur baaki ko song ka trigger manenge
    target_user = cmd[-1]
    trigger_key = " ".join(cmd[1:-1]).lower()

    if trigger_key not in SONGS_DB:
        await message.edit(f"`Song not found! Tune ye first line save nahi ki hai: {trigger_key}`")
        await asyncio.sleep(3)
        await message.delete()
        return

    song_data = SONGS_DB[trigger_key]
    delay = song_data["delay"]
    original_first_line = song_data["first_line"]

    # Delete the command message
    await message.delete()

    # Pehli line send karna user ko tag karke
    await client.send_message(message.chat.id, f"{target_user} {original_first_line}")

    # Baaki ki lines loop me delay ke sath
    for line in song_data["lines"]:
        await asyncio.sleep(delay)
        await client.send_message(message.chat.id, f"{target_user} {line}")


