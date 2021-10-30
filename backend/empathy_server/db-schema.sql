-- Stories table for Practice Empathy Needs Database.
-- From: https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS needs;
DROP TABLE IF EXISTS stories;

-- rooms table maps a unique (over all time) room index to a room key.
-- the room key is unique among all current rooms, but probably not
-- unique across all time.
-- room IDs are never re-used (even after rooms are deleted)
CREATE TABLE rooms (
  room_index INTEGER PRIMARY KEY AUTOINCREMENT,
  room_key VARCHAR(4)
);

-- Main needs table: tracks needs recorded, including which room they were
-- recorded in.
-- AUTO_INCREMENT not needed, per notes here: https://sqlite.org/autoinc.html
CREATE TABLE needs (
  need_index INTEGER PRIMARY KEY,
  room_index INTEGER NOT NULL,
  need VARCHAR(30) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (room_index) REFERENCES rooms(room_index)
);

-- Beyond this point... old tables used in earler iteration of DB.

-- Main stories table: tracks needs recorded against each story
-- Notes:
-- AUTO_INCREMENT not needed, per notes here: https://sqlite.org/autoinc.html
CREATE TABLE stories (
  row_index INTEGER PRIMARY KEY,
  story_id INTEGER NOT NULL,
  need VARCHAR(30) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  weight INTEGER NOT NULL CHECK (weight > 0 AND weight < 5),
  time1 INTEGER NOT NULL CHECK (time1 >= 0),
  time2 INTEGER CHECK (time2 >= 0),
  time3 INTEGER CHECK (time3 >= 0),
  time4 INTEGER CHECK (time4 >= 0)
);

-- Index used to accelerate searches for needs recorded against a particular story.
CREATE INDEX idx_story_index
ON stories (story_id, need);

-- Index used to accelerate searches based on creation time.
CREATE INDEX idx_row_created
ON stories (created);
