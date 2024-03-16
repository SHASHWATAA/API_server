import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel

import HomeAssistant
import Deputy
import Hackathon

app = FastAPI()
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

class User(BaseModel):
    user: str


@app.post("/hackathon/{authentication_token}/super-user/")
async def dummy_data_print(authentication_token: str, user: User):
    # if authentication_token == 'cu7igeg7cl':
    #     pass
    # else:
    #     return "{error:authentication failed}"

    print(User)
    # return data

    # Hackathon.checklist_create(data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9530, reload=False)
