import json
import os
from pakages import app 

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)
    
def load_categories():
    return read_json(os.path.join(app.root_path, "data/Categories.json"))
    
def load_conferences(cats):
    if cats == 1:
        return load_deadline()
    elif cats == 2:
        return load_running()
    elif cats == 3:
        return load_future()
    else:
        return load_planned()

def load_deadline():
    return read_json(os.path.join(app.root_path, "data/Deadline_ahead.json"))

def load_running():
    return read_json(os.path.join(app.root_path, "data/Running_conferences.json"))

def load_future():
    return read_json(os.path.join(app.root_path, "data/Future_conferences.json"))

def load_planned():
    return read_json(os.path.join(app.root_path, "data/Planned_conferences.json"))




# file nay chua cac ham tuong tac voi data