# db.py

import json
import os

DB_PATH = "database/data.json"

def load_data():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def add_points(user_id, amount):
    data = load_data()
    data[user_id] = data.get(user_id, 0) + amount
    save_data(data)

def get_points(user_id):
    data = load_data()
    return data.get(user_id, 0)