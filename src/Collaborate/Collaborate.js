import React from "react";
import { useState } from "react";
const ROLE_LEADER = 1
const ROLE_PARTICIPANT = 2


export function CollaborateTab(props) {

    var html

    if (props.room) {
      if (props.role === ROLE_LEADER) {
        html = (
        <>
          <RoomHeader
           room = {props.room}/>
          <RoomResults/>
        </>
        )
      }
      else {
        console.assert(props.role === ROLE_PARTICIPANT)
        html = (
          <>
            <RoomHeader
             room = {props.room}/>
            <NeedsPicker/>
          </>
        )
      }
    }
    else {
      html = (
        <>
          <CreateRoom
           setRoom = {props.setRoom}
           setRole = {props.setRole}/>
          <EnterRoom
           setRoom = {props.setRoom}
           setRole = {props.setRole}/>
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

      return fetch('http://127.0.0.1:5000/needs/new_room', {
                   method: 'POST',
                   headers: {
                     'Accept': 'application/json',
                     'Content-Type': 'application/json'
                   },
                 })
        .then(response => response.json())
        .then(data => {
          props.setRoom(data['key'])
          props.setRole(ROLE_LEADER)
        });
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
