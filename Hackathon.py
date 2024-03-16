from typing import List
from pydantic import BaseModel
import json
import sqlite3

conn = sqlite3.connect('Hackathon.db')

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS CheckList (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    completed BOOLEAN,
    reward_type INTEGER,
    task_ids TEXT
)''')


class Task(BaseModel):
    id: int
    name: str
    checklist_id: int
    description: str
    completed: bool


class Reward(BaseModel):
    id: int
    name: str
    description: str


class CheckList:
    def __init__(self, id, name, description, completed, reward_type, task_ids):
        self.id = id
        self.name = name
        self.description = description
        self.completed = completed
        self.reward_type = reward_type
        self.task_ids = task_ids

def checklist_create(data):
    data_json = json.loads(data)
    task_list = data_json['tasks_list']
    data_json['task_ids'] = ''.join(str(x['id']) + "," for x in task_list)
    data_json.pop('tasks_list', None)
    checklist_instance = CheckList(**data_json)

    conn.cursor().execute(
        'INSERT INTO CheckList (id, name, description, completed, reward_type, task_ids) VALUES (?, ?, ?, ?, ?, ?)',
        (checklist_instance.id, checklist_instance.name, checklist_instance.description,
         checklist_instance.completed, checklist_instance.reward_type, checklist_instance.task_ids)
    )


    pass


if __name__ == '__main__':
    data = '{"id":1,"name":"chores","description":"home chores","completed":"False", "reward_type":1,"tasks_list":[{"id":1,"name":"Do dishes","description":"keep all dishes in the sync in the dishwasher and empty, dry and place them where they belong when it finishes.","completed":"False"},{"id":2,"name":"Do Homework","description":"Finish all homework and put it in your bag","completed":"False"}]}'
    checklist_create(data=data)
