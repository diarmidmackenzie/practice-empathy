import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import random
import string

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('db-schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def random_key():
    letters = string.ascii_uppercase
    key = (''.join(random.choice(letters) for i in range(4)))
    return key

def db_create_room():

    # Pick a new key for the room.
    room_key = random_key()

    ## TO DO - logic to de-duplicate clashing keys...

    values = (room_key,)
    print(values)
    sql_command = """INSERT INTO rooms
                     (room_key)
                     VALUES (?);"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql_command, values)
    db.commit()

    return cursor.lastrowid, room_key

def db_room_needs(room_id):
    db = get_db()
    cursor = db.cursor()
    values = (room_id,)
    query = """SELECT need, created FROM needs
               WHERE room_index = ?"""
    cursor.execute(query, values)

    rows = cursor.fetchall()
    print("DB ROWS:")
    print(rows)

    # Config sets might have clashing MS Indices
    # So we sort  by db_index, and include MS Index as an additional property.
    needs = []
    for row in rows:
        print(row)
        print(row.keys)
        need = {'need' : row['need'],
                'timestamp' : row['created']}
        needs.append(need)

    return (needs)

def db_add_need_row(room_id, need):

    values = (room_id, need)
    sql_command = """INSERT INTO needs
                     (room_index, need)
                     VALUES (?, ?);"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql_command, values)
    db.commit()

    return cursor.lastrowid

# subsequent code implements old version of db - probably will be deprecated
# in future.


# db is the SQL DATABASE
# story_id is the numberical id for the
# need is the text of the need
# time_data is a list of times: [time1, time2,..]
def db_add_row(story_id, need, times):
    # Note that row_index & creation timestamp can be left as default
    # The SQL DB will set them correctly.
    print(times)

    sql_command = "INSERT INTO STORIES (story_id, need, weight"
    for ii in range(0, len(times)):
        sql_command += ", time%d" % (ii + 1)

    sql_command += ") VALUES (%d, \"%s\", %d" % (story_id, need, len(times))

    for ii in range(0, len(times)):
        sql_command += ", %d" % times[ii]

    sql_command += ");"
    print(sql_command)

    db = get_db()
    db.execute(sql_command)
    db.commit()

    return

def db_list_needs_and_weights(story_id):
  db = get_db()

  cursor = db.cursor()
  cursor.execute("SELECT need, weight FROM stories WHERE story_id = %d" % story_id)
  rows = cursor.fetchall()

  needs = []
  weights = []
  for row in rows:
      need = row['need']
      weight = row['weight']
      print(need, weight)

      # Either this is a new need, or one we have seen before (already in list).

      try:
          index = needs.index(need)
      except:
          index = -1

      if index == -1:
          # Not yet in list - add it & its weight.
          assert(len(needs) == len(weights))
          needs.append(need)
          weights.append(weight)
      else:
          # We has already identified this need.
          # Just add the weight.
          weights[index] += weight

  return (needs, weights)
