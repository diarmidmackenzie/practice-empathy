# Some basic smoke tests so far for the HTTP API.
# Lots missing including negative testcases (e.g. illegal parameters)
# Some design work needed to think how best to structure as we add more test cases...
# To run:
# In practice-empathy/backend/test directory.
# Run: python -m pytest test_empathy_server.py

import requests
import json
import pytest
import os
import subprocess

def new_room():

    response = requests.post("http://127.0.0.1:5000/needs/new_room", headers = {'Content-Type': "application/json"}, data = "")
    assert response.status_code == 200

    json_text = response.text
    dict = json.loads(json_text)
    id = dict['id']
    key = dict['key']

    return id, key

def example_post(room_id):

    data = {'room': room_id, 'need': "air"}
    json_data = json.dumps(data)

    response = requests.post("http://127.0.0.1:5000/needs/add_need", headers = {'Content-Type': "application/json"}, data = json_data)
    assert response.status_code == 200
    return

def example_get(room_id):
    response = requests.get(f"http://127.0.0.1:5000/needs/needs?room={room_id}")

    assert response.status_code == 200
    json_text = response.text
    dict = json.loads(json_text)
    need = dict[0]['need']
    timestamp = dict[0]['timestamp']

    assert need == "air"

def get_room_id(room_key, id):
    response = requests.get(f"http://127.0.0.1:5000/needs/room_id?room_key={room_key}")

    assert response.status_code == 200
    json_text = response.text
    dict = json.loads(json_text)
    room_id = dict['id']
    assert room_id == id

def example_old_post():
    needs = ["air", "inclusion", "food", "air", "air", "nurture"]
    times = [15, 33, 44, 46, 62, 124]
    story = 1
    data = {'story': 1, 'needs': needs, 'times': times}

    json_data = json.dumps(data)

    response = requests.post("http://127.0.0.1:5000/needs/submit", headers = {'Content-Type': "application/json"}, data = json_data)

    assert response.status_code == 200
    return

def example_old_get():
    response = requests.get("http://127.0.0.1:5000/needs/list?story=1")

    assert response.status_code == 200
    json_text = response.text
    dict = json.loads(json_text)
    needs = dict['needs']
    weights = dict['weights']

    # Needs seem to always come back in alphabetical order.
    # TBD whether that's a bug...!
    assert needs[0] == "air"
    assert needs[1] == "food"
    assert needs[2] == "inclusion"
    assert needs[3] == "nurture"
    assert weights[0] == 3
    assert weights[1] == 1
    assert weights[2] == 1
    assert weights[3] == 1
    return

def example_old_post_with_spaces():
    needs = ["to be heard", "to be seen", "a a a a a a a a a a a", "a a a a a a a a a a a"]
    times = [10, 20, 30, 40]
    story = 2
    data = {'story': story, 'needs': needs, 'times': times}

    json_data = json.dumps(data)

    response = requests.post("http://127.0.0.1:5000/needs/submit", headers = {'Content-Type': "application/json"}, data = json_data)

    assert response.status_code == 200
    return

def example_old_get_with_spaces_scaled(count):
    response = requests.get("http://127.0.0.1:5000/needs/list?story=2")

    assert response.status_code == 200
    json_text = response.text
    dict = json.loads(json_text)
    needs = dict['needs']
    weights = dict['weights']

    # Needs seem to always come back in alphabetical order.
    # TBD whether that's a bug...!
    assert needs[0] == "a a a a a a a a a a a"
    assert needs[1] == "to be heard"
    assert needs[2] == "to be seen"
    assert weights[0] == 2 * count
    assert weights[1] == count
    assert weights[2] == count
    return

def initialize_environment():
    # Initialize (clear) database (flask server started separately)
    os.putenv('FLASK_APP', "empathy_server")
    # Flask server must be run from "backend" directory, one level up from "test".
    os.chdir("..")
    subprocess.run(['python', '-m', 'flask', 'init-db'])
    flask_process = subprocess.Popen(['python', '-m', 'flask', 'run'])

    # Move back to "test" directory, so that we are in the same state that
    # we started in.
    os.chdir("test")

    return flask_process

# Tests 1 & test 2 test the old API. (still supported but deprecated)
def test_1():
    flask_process = initialize_environment()
    example_old_post()
    example_old_get()
    flask_process.terminate()

def test_2():
    # covers needs with spaces.  Also scaling to 10 records.
    flask_process = initialize_environment()
    for i in range(10):
        example_old_post_with_spaces()

    example_old_get_with_spaces_scaled(10)
    flask_process.terminate()

# Tests 3 & beyond test the new API.
def test_3():
    flask_process = initialize_environment()
    room_id, room_key = new_room()
    get_room_id(room_key, room_id)
    example_post(room_id)
    example_get(room_id)
    flask_process.terminate()
