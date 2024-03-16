from typing import List
from pydantic import BaseModel
import json

class Task(BaseModel):
    id: int
    name: str
    description: str
    completed: bool


class Reward(BaseModel):
    id: int
    name: str
    description: str


class CheckList(BaseModel):
    id: int
    name: str
    description: str
    completed: bool
    reward_type: int
    tasks_list: List[Task]


def checklist_create(data: CheckList):
    data_json = json.loads(data)

    checklist_instance = CheckList(**data_json)

    pass

