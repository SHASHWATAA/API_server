# user_routes.py
from fastapi import APIRouter
import credentials
from discord_bot.discord_bot import bot

router = APIRouter()


# Define a FastAPI route that accepts a parameter
@router.get("/discord-bot/send-message")
async def send_to_channel(message: str, channel_id: int):
    # Replace "your_channel_id" with the actual channel ID where you want to send the message
    # channel_id = credentials.channel_id  # Example channel ID
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(message)
        return {"status": "Message sent successfully!"}
    else:
        return {"error": "Channel not found."}
