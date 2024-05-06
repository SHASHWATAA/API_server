# user_routes.py
from typing import List

from fastapi import APIRouter, Query

from discord_bot.discord_bot import bot, send_images

router = APIRouter()


# Define a FastAPI route that accepts a parameter
@router.post("/discord-bot/send-message")
async def send_to_channel(message: str, channel_id: int):
    # Replace "your_channel_id" with the actual channel ID where you want to send the message
    # channel_id = credentials.channel_id  # Example channel ID
    channel = bot.get_channel(channel_id)

    if channel:
        message = await channel.send(message)
        return {"status": f"Message sent successfully!",
                "message_id": message.id}
    else:
        return {"error": "Channel not found."}


@router.post("/discord-bot/send-images")
async def send_to_channel(channel_id: int, image_paths: List[str] = Query(...)):
    print(image_paths)
    # Replace "your_channel_id" with the actual channel ID where you want to send the message
    # channel_id = credentials.channel_id  # Example channel ID
    await send_images(image_paths, channel_id)


@router.post("/discord-bot/add-reaction")
async def add_reaction_to_message(message_id: int, channel_id: int, reaction: str):
    # Replace 'your_bot' with your actual bot instance
    message = await bot.get_channel(channel_id).fetch_message(message_id)

    if message:
        try:
            await message.add_reaction(reaction)
            return {"status": "Reaction added successfully!"}
        except Exception as e:
            return {"error": f"Error adding reaction: {str(e)}"}
    else:
        return {"error": "Message not found."}
