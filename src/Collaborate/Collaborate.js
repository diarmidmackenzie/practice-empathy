import React from "react";
import { useState } from "react";
const ROLE_LEADER = 1
const ROLE_PARTICIPANT = 2


export function CollaborateTab(props) {

    const [room, setRoom] = useState("");
    const [role, setRole] = useState(0);

    var html

    if (room) {
      if (role === ROLE_LEADER) {
        html = (
        <>
          <RoomHeader
           room = {room}/>
          <RoomResults/>
        </>
        )
      }
      else {
        console.assert(role === ROLE_PARTICIPANT)
        html = (
          <>
            <RoomHeader
             room = {room}/>
            <NeedsPicker/>
          </>
        )
      }
    }
    else {
      html = (
        <>
          <CreateRoom
           setRoom = {setRoom}
           setRole = {setRole}/>
          <EnterRoom
           setRoom = {setRoom}
           setRole = {setRole}/>
        </>
      )
    }

    return (
      <>
      {html}
      </>
    )
}

function CreateRoom(props) {

    function generateRoomId() {

      var roomID = "ABCD"
      props.setRoom(roomID)
      props.setRole(ROLE_LEADER)
    }

    return (
    <>
      <button onClick={() => generateRoomId()}>Create Room</button>
    </>
    )
}

function EnterRoom(props) {

    const [roomID, setRoomID] = useState('');

    function handleChange(event) {
      setRoomID(event.target.value);
    }

    function handleSubmit() {

      props.setRoom(roomID)
      props.setRole(ROLE_PARTICIPANT)
    }

    return (
      <>
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input type="text" value={roomID} onChange={handleChange} />
          </label>
          <input type="submit" value="Enter Room" />
        </form>
      </>
    )
}

function RoomHeader(props) {

    return (
    <div>
      Room ID: {props.room}
    </div>
    )
}

function NeedsPicker(props) {

    return (
    <div>
      Select Needs
    </div>
    )
}

function RoomResults(props) {

    return (
    <div>
      Room Results
    </div>
    )
}
