import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException
import HomeAssistant

app = FastAPI()
websocket_app = None


@app.get("/home-assistant/turn-on-tv", status_code=200)
async def turn_on_tv():
    tv_state = HomeAssistant.turn_on_tv(HomeAssistant.living_room_tv_entity_id, HomeAssistant.ha_authorization_headers)
    if tv_state != "on":
        raise HTTPException(status_code=424, detail="TV didn't turn on.")

    return "tv turned on"


@app.get("/home-assistant/turn-off-tv", status_code=200)
async def turn_on_tv():
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=9530, reload=True)
