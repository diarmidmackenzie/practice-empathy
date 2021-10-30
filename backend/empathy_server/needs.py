import functools
import time
import json
from flask import (
    Blueprint, request, jsonify
)
from empathy_server.db import (get_db,
                               db_add_row,
                               db_list_needs_and_weights,
                               db_create_room,
                               db_room_needs,
                               db_add_need_row)

bp = Blueprint('needs', __name__, url_prefix='/needs')

@bp.route('/')
def hello_world():
    return 'Hello, this is the Empathy Server!'

@bp.route('/needs')
def room_needs():
# Request of form: /needs?room_id=123
#    json = """
#    [
#      {need: "air", timestamp: <timestamp>},
#      {need: "inclusion", timestamp: <timestamp>},
#      {need: "air", timestamp: <timestamp>},
#   ]
    print("GET: /needs")
    room = request.args.get('room_id')

    try:
        room_id = int(room)
        assert(room_id > 0)
    except:
        # Invalid or missing parameter
        print("Invalid parameter: " + room_id)
        return("{}")

    needs = db_room_needs(room_id)

    return needs


@bp.route('/add_need', methods = ['POST'])
def add_need():
    print("POST: /add_need")

    json_data = request.json
    text = process_need(json_data)
    return text

@bp.route('/new_room', methods = ['POST'])
def new_room():
    print("POST: /new_room")
    room_data = process_new_room()
    return room_data

def process_new_room():

    id, key = db_create_room()

    room_data = {'id': id, 'key': key}

    return room_data

# JSON to process should be of the following form.
# {
#      "room": 123,
#      "need": "air"
# }
def process_need(data):
    print(data)
    room_id = data['room']
    need = data['need']

    db_add_need_row(room_id, need)

    text = "OK"
    return text


# This later code implements an earlier version of the backend.
# Currently maintained in parallel, but may be retired in future.

@bp.route('/list')
def needs_list():
# Request of form: /list?story=1
#    json = """
#    {
#   "needs":[
#      "air",
#      "inclusion",
#      "food",
#      "nurture"
#   ],
#   "weights":[
#      1,
#      2,
#      5,
#      10
#   ]
#}
    print("GET: /list")
    story = request.args.get('story')

    try:
        story_id = int(story)
        assert(story_id > 0)
    except:
        # Invalid or missing parameter
        print("Invalid parameter: " + story)
        return("{}")

    (needs, weights) = db_list_needs_and_weights(story_id)
    dictionary = {'needs': needs, 'weights': weights}
    json_text = json.dumps(dictionary)

    return (json_text)

@bp.route('/submit', methods = ['GET', 'POST'])
def needs_submission():
    print("GET or POST: /submit")
    if request.method == 'POST':
        print("POST: /submit")
        json_data = request.json
        text = process_submission(json_data)
        return text

# JSON to process should be of the following form.
# {
#      "story": 1,
#      "needs":[
#      "air",
#      "inclusion",
#      "food",
#      "air",
#      "air",
#      "nurture"
#   ],
#   "times":[
#      15,
#      33,
#      44,
#      46,
#      62,
#      124
#   ]
# }

def process_submission(data):
    print(data)
    story = data['story']
    needs = data['needs']
    times = data['times']

    # Run some checks on the data.

    try:
        assert(len(needs) == len(times))
        # TBD what other checks we can do...
    except:
        print ("Invalid JSON data")
        return False

    # Generate consolidated disctionary of needs & weights.
    # Key = need name.
    # Data = a list of times: [time1, time2,..]
    needs_dict = {}
    for ii in range(len(needs)):
        need = needs[ii]
        if need in needs_dict:
            # Need already in dictionary.
            # Find out how many times we have already recorded, and add the next
            # in the next spare slot.
            assert(len(needs_dict[need]) > 0)
            assert(len(needs_dict[need])  < 4)
            needs_dict[need].append(times[ii])
        else:
            # Need not yet in dictionary, add it.
            needs_dict[need] = [times[ii]]

    # We now have a dictionary of data tuples to add to the dictionary
    # Each to be added as a row, along with the story id (key) and the need.
    for key, value in needs_dict.items():
        db_add_row(story, key, value)

    text = "OK"
    return text
