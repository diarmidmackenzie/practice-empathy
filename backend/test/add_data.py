# Assumes flask server already running at 127.0.0.1:5000
import requests
import json
import pytest
import os
import subprocess

def example_post():
    needs = ["air", "inclusion", "food", "air", "air", "nurture"]
    times = [15, 33, 44, 46, 62, 124]
    story = 1
    data = {'story': 1, 'needs': needs, 'times': times}

    json_data = json.dumps(data)

    response = requests.post("http://127.0.0.1:5000/needs/submit", headers = {'Content-Type': "application/json"}, data = json_data)

    assert response.status_code == 200
    return
    
example_post()
