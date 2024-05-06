from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException
import HomeAssistant
import Deputy
import discord_bot.FastAPI_user_routes
import invoice_generator.FastAPI_user_routes
app = FastAPI()
app.include_router(discord_bot.FastAPI_user_routes.router)
app.include_router(invoice_generator.FastAPI_user_routes.router)
websocket_app = None


@app.get("/home-assistant/turn-on-tv", status_code=200)
async def turn_on_tv():
    tv_state = HomeAssistant.turn_on_tv(HomeAssistant.living_room_tv_entity_id, HomeAssistant.ha_authorization_headers)
    if tv_state != "on":
        raise HTTPException(status_code=424, detail="TV didn't turn on.")

    return "tv turned on"


@app.get("/home-assistant/turn-off-tv", status_code=200)
async def turn_off_tv():
    tv_state = HomeAssistant.turn_off_tv(HomeAssistant.living_room_tv_entity_id, HomeAssistant.ha_authorization_headers)
    if tv_state != "off":
        raise HTTPException(status_code=424, detail="TV didn't turn off.")

    return "tv turned off"


@app.get("/home-assistant/switch-source-to-plex")
async def switch_source_to_plex():
    status_code = HomeAssistant.switch_tv_to_plex(HomeAssistant.living_room_tv_entity_id)
    if status_code != 200:
        raise HTTPException(status_code=424, detail="TV didn't turn on.")

    return "plex turned on"


@app.get("/home-assistant/movie-time")
async def movie_time():
    status = HomeAssistant.movie_time(HomeAssistant.living_room_tv_entity_id, headers=HomeAssistant.ha_authorization_headers)
    if not status:
        raise HTTPException(status_code=424, detail="TV didn't turn on or Plex coudn't open.")

    return "plex turned on"


@app.get("/deputy/start-shift")
async def start_shift():
    Deputy.start_shift()

    return "shift started"


@app.get("/deputy/end-shift/{end_time}")
async def end_shift(end_time: str):
    Deputy.end_shift(end_time)

    return end_time
