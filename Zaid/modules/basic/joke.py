import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid import SUDO_USER


@Client.on_message(filters.command("joke", ".") & (filters.me | filters.user(SUDO_USER)))
async def joke_cmd(client: Client, message: Message):
    m = await message.reply_text("😏 Searching best joke for you...")

    steps = ["😏", "🤔", "🤣", "😂"]
    for step in steps:
        await m.edit_text(step)
        await asyncio.sleep(0.6)

    jokes = [
        "🤣 Teacher: Tum itne late kyun aaye?\n😎 Student: Sir, exam me likhne layak kuch tha hi nahi, isliye timepass kar raha tha.",
        "😂 Pappu: Doctor sahab, mujhe bhoolne ki bimari ho gayi hai!\n👨‍⚕️ Doctor: Kab se?\n🤔 Pappu: Kab se kya?",
        "🤣 Girlfriend: Tum mujhe gift me kya doge?\n😏 Boyfriend: Tumhe pasand aa gaya to shaadi kar lunga… warna wapas kar dunga!",
        "😂 Ek dost: Yaar, teri watch kaha se li?\n😎 Dusra dost: Time bataane wale app se!",
        "🤣 Pappu: Mujhe lottery lag gayi!\n😲 Friend: Kitne ki?\n😏 Pappu: 100rs ki ticket kharidi thi, 50rs jeet gaya!",
        "😂 Teacher: Tumhare exam ke number itne kam kyun aaye?\n😎 Student: Kyunki paper hi easy tha, mushkil hota to zyada likhta!",
        "🤣 Wife: Suno ji, main kitni moti lagti hoon?\n😏 Husband: Tum Moti nahi ho… Tum to Full HD ho!",
        "😂 Pappu: Mere phone me network nahi aa raha!\n🤣 Friend: Shaadi kar le, biwi roz ‘network’ banake baithegi!",
        "🤣 Doctor: Aapko diabetes ho gayi hai.\n😲 Patient: Kab se?\n😂 Doctor: Jab se aapne apni girlfriend ka naam ‘Mithu’ rakha hai!",
        "😂 Santa: Train late kyu hai?\n🤣 Guard: Track me kachua chal raha tha!\n😏 Santa: Usse utaar dete, main uski jagah bhaag leta!",
        "🤣 Pappu: Papa mujhe exam me 100% mile hain!\n😲 Papa: Sach?\n😂 Pappu: Haan, 10 subjects me 10–10%!",
        "😂 Teacher: 1 aur 1 kitna hota hai?\n🤣 Student: Sir, pyar me to 11 ho jata hai!",
        "🤣 Pappu: Bhai, tumhari biwi bhag gayi!\n😂 Friend: Achha hua… recharge khatam ho gaya tha!",
        "😂 Santa: Kal sapne me TV chal raha tha!\n🤣 Banta: Kaisa show dekh raha tha?\n😏 Santa: Remote hi nahi mila!",
        "🤣 Biwi: Mujhe ek aisi jagah le chalo jaha shanti ho!\n😂 Pati: Chalo tumhe library le chalta hoon!",
        "😂 Student: Sir, light nahi thi isliye homework nahi bana!\n🤣 Teacher: Kya tumhe candle bhi nahi mili?\n😏 Student: Candle mili thi sir, lekin uski light me padhne ka mood nahi ban raha tha!",
        "🤣 Dost: Tere ghar me wifi hai?\n😂 Dusra: Haan, password hai ‘bhikmange’!\n🤣 Dost: Achha bhikmange kya?\n😏 Dusra: Password hi hai yaar!",
        "😂 Teacher: Padhayi kyun nahi karte?\n🤣 Student: Sir, future bright karne ke liye padhayi karta hoon… lekin bijli department ne already future bright kar diya hai!",
        "🤣 Wife: Tum mujhe kabhi shopping pe nahi le jaate!\n😂 Husband: Arre main to soch raha tha tumhara kidnapping ho jaye aur shopping free ho jaye!",
        "😂 Pappu: Mere phone ka balance khatam ho gaya!\n🤣 Friend: To girlfriend se baat kaise karega?\n😏 Pappu: Uske hi number pe miss call maar ke boloonga, recharge kar de!",
        "🤣 Teacher: Tum paper me kya likh ke aaye the?\n😂 Student: Sir, Bhagwan bharose chhod diya tha!\n😏 Teacher: Bhagwan bhi hairan hai tumhare handwriting dekh ke!",
        "🤣 Wife: Tum mujhe miss karte ho?\n😂 Husband: Haan, jab tum bolti ho ‘shopping chalo’ tab miss kar deta hoon!",
        "😂 Santa: Yaar mujhe lottery me gaadi mili!\n🤣 Banta: Kaisi?\n😏 Santa: Pedal wali!",
        "🤣 Dost: Tere ghar me fridge hai?\n😂 Dusra: Haan, par woh sirf naam ka hai!\n😏 Dost: Matlab?\n🤣 Dusra: Kyunki andar sirf hawa hai!",
        "😂 Pappu: Sir, exam ke question paper me galti thi!\n🤣 Teacher: Kaise?\n😏 Pappu: Ussme answers hi nahi the!",
        "🤣 Wife: Tum mujhe kab pyaar karna band karoge?\n😂 Husband: Jab tumhe free me recharge milna band ho jaayega!",
        "😂 Santa: Mere computer me virus aa gaya!\n🤣 Banta: Kya karoge?\n😏 Santa: Usko Dettol lagaunga!",
        "🤣 Dost: Tu itna handsome kaise ban gaya?\n😂 Dusra: Filter lagake!",
        "😂 Student: Sir, main paper me fail ho gaya!\n🤣 Teacher: Kyun?\n😏 Student: Kyunki paper English me tha, aur main Hindi medium ka hoon!",
        "🤣 Wife: Tum itna mobile kyun chalate ho?\n😂 Husband: Kyunki usme tumse zyada battery hai!"
    ]

    joke = random.choice(jokes)
    await m.edit_text(joke)
