from motor.motor_asyncio import AsyncIOMotorClient

# Use same MONGO_URI as project
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["ZaidRobot"]
botban = db.botban

async def is_botbanned(user_id: int):
    return await botban.find_one({"user_id": user_id})

async def botban_user(user_id: int):
    await botban.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def botunban_user(user_id: int):
    await botban.delete_one({"user_id": user_id})

async def botban_list():
    return botban.find({})
