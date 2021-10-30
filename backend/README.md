# Translations REST API Documentation



## API Endpoints

All API endpoints are under /needs/

This section lists available endpoints, together with sample output, showing the structure of the data.



### /new_room

Method: POST

Create a new room, which is a private partition within which needs data can be shared.

Returns JSON data that looks like this:

```
{'id': 1, 'key': ABCD}
```

The room id (numeric) is the identifier that should be used on API calls.

The room key should be used by users wanting to log into a room.  As a 4 character (upper-case) string, it is intended to be both harder to guess, and easier to remember, than a numeric ID.

*FUTURE: these strings will be guaranteed unique in terms of current live rooms.  They won't be unique across all time.*



### /room_id?room_key={key}

Method: GET

Provides a room id from a room key.

Returns data like this:

```
{'id': 1}
```

Used by non-hosting clients to get the room id to use on this API.  This ID will be fixed for the lifetime of the room.



### /add_need

Method: POST

POST should include JSON data like this:

```
{'room' : {room id}, 'need': {need text}}
```

No data returned other than a response code indicating success (or failure).

This adds a need for this room to the database.

The same need can be added multiple times.  However, individual clients should be responsible for only adding each need once.  Different clients can absolutely add the same need as each other.

The server stores the timestamp when the need was added, which can be served up later (see /needs endpoint).



### /needs?room={room id}

Method: GET

```
[
   {
      "need":"Acknowledgment",
      "timestamp":"2021-10-30 18:38:00"
   },
   {
      "need":"Mourning",
      "timestamp":"2021-10-30 18:38:05"
   },
   {
      "need":"Friendship",
      "timestamp":"2021-10-30 18:38:05"
   }
]
```



### FUTURE API

delete need

delete room

record which client added which need?

info on number of clients connected?

security, robustness...

???



### LEGACY API

In the code, we also have the "stories" endpoint from a previous iteration of this project.  This is deprecated, so not documented here.
