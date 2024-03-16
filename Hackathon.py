import pickle
from typing import List
from pydantic import BaseModel
import json
import sqlite3


class Task(BaseModel):
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


def checklist_create(checklist_data):
    conn = sqlite3.connect('Hackathon.db')
    cursor = conn.cursor()

    # Execute the CREATE TABLE statement
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CheckList (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            completed BOOL,
            reward_type INTEGER,
            tasks_list BLOB
        );
    ''')

    # Insert data into the table
    cursor.execute('''
        INSERT INTO CheckList (name, description, completed, reward_type, tasks_list)
        VALUES (?, ?, ?, ?, ?);
    ''', (
        checklist_data.name,
        checklist_data.description,
        checklist_data.completed,
        checklist_data.reward_type,
        pickle.dumps(checklist_data.tasks_list)  # Serialize the tasks list
    ))

    assigned_id = cursor.lastrowid
    # print(assigned_id)
    conn.commit()
    conn.close()
    return assigned_id


def update_checklist_data(checklist_id, checklist_data):
    conn = sqlite3.connect('Hackathon.db')
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('SELECT * FROM CheckList WHERE id = ?', (checklist_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        # Perform an UPDATE
        cursor.execute('''
            UPDATE CheckList
            SET name = ?, description = ?, completed = ?, reward_type = ?, tasks_list = ?
            WHERE id = ?;
        ''', (
            checklist_data.name,
            checklist_data.description,
            checklist_data.completed,
            checklist_data.reward_type,
            pickle.dumps(checklist_data.tasks_list),
            checklist_id
        ))
    conn.commit()
    conn.close()
    assigned_id = checklist_id
    return retrieve_checklist_data(assigned_id)


def retrieve_checklist_data(assigned_id):
    conn = sqlite3.connect('Hackathon.db')
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve the row with the given assigned_id
    cursor.execute('SELECT id, name, description, completed, reward_type, tasks_list FROM CheckList WHERE id = ?', (assigned_id,))
    row = cursor.fetchone()

    if row:
        id, name, description, completed, reward_type, serialized_tasks_list = row

        # Deserialize the tasks_list
        tasks_list = pickle.loads(serialized_tasks_list)

        # Create an instance of CheckList
        checklist_data = CheckList(
            id=id,
            name=name,
            description=description,
            completed=completed,
            reward_type=reward_type,
            tasks_list=[dict(x) for x in tasks_list]
        )

        conn.close()
        return checklist_data
    else:
        conn.close()
        return None  # No data found for the given assigned_id


if __name__ == '__main__':
    data = '{"id":1,"name":"chores","description":"home chores","completed":"False", "reward_type":1,"tasks_list":[{"id":1,"name":"Do dishes","description":"keep all dishes in the sync in the dishwasher and empty, dry and place them where they belong when it finishes.","completed":"False"},{"id":2,"name":"Do Homework","description":"Finish all homework and put it in your bag","completed":"False"}]}'
    checklist_create(data=data)
