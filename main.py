from typing import List, Dict

import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel

import HomeAssistant
import Deputy
import Hackathon
from fastapi.staticfiles import StaticFiles
from os import listdir, walk, path
from os.path import isfile, join
from typing import List
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow credentials (e.g., cookies, authorization headers)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

websocket_app = None
app.mount("/images/", StaticFiles(directory="images"), name="images")


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


class Task(BaseModel):
    name: str
    description: str
    completed: bool


class CheckList(BaseModel):
    name: str
    description: str
    completed: bool
    reward_type: int
    tasks_list: List[Task]


@app.post("/hackathon/{authentication_token}/super-user/")
async def create_checklist(checklist: CheckList, authentication_token: str):
    if authentication_token == 'cu7igeg7cl':
        pass
    else:
        return "{error:authentication failed}"

    print(checklist)

    checklist_id = Hackathon.checklist_create(checklist)

    checklist_data = Hackathon.retrieve_checklist_data(checklist_id)

    return checklist_data


@app.get("/hackathon/{authentication_token}/super-user/{id}")
async def create_checklist(authentication_token: str, id: int):
    if authentication_token == 'cu7igeg7cl':
        pass
    else:
        return "{error:authentication failed}"

    return Hackathon.retrieve_checklist_data(id)


@app.put("/hackathon/{authentication_token}/super-user/{checklist_id}")
async def update_checklist(checklist: CheckList, authentication_token: str, checklist_id: int):
    if authentication_token == 'cu7igeg7cl':
        pass
    else:
        return "{error:authentication failed}"

    print(checklist)

    checklist_data = Hackathon.update_checklist_data(checklist_id, checklist)

    return checklist_data


def get_image_structure(directory: str) -> Dict[str, List[Dict[str, List[str]]]]:
    image_structure = {}
    for root, dirs, files in walk(directory):
        dir_name = path.basename(root)
        if dir_name not in image_structure:
            image_structure[dir_name] = []
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                image_structure[dir_name].append(filename)
    return image_structure


@app.get("/images", response_model=Dict[str, List[Dict[str, List[str]]]])
def list_image_structure():
    image_dir = "images"  # Path to your Hackathon directory
    image_structure = get_image_structure(image_dir)
    return {"images": [image_structure]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9530, reload=True)
