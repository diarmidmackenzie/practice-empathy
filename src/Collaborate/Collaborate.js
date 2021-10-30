import React from "react";
import { useState } from "react";
import * as constants from "../Needs/needs";

const ROLE_LEADER = 1
const ROLE_PARTICIPANT = 2

function CheckError(response) {
  if (response.status >= 200 && response.status <= 299) {
    return response.json();
  } else {
    throw Error(response.statusText);
  }
}

export function CollaborateTab(props) {

    var html

    if (props.room.key) {
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
            <NeedsPicker
             room = {props.room}/>
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
        .then(CheckError)
        .then(data => {
          props.setRole(ROLE_LEADER)
          props.setRoom({key: data['key'], id: data['id']})
        });
    }

    return (
      <>
        <button onClick={() => generateRoomId()}>Create Room</button>
      </>
    )
}

function EnterRoom(props) {

    const [tempRoomKey, setTempRoomKey] = useState('');
    const [errorText, setErrorText] = useState('');

    function handleChange(event) {
      setTempRoomKey(event.target.value);
    }

    function handleSubmit(event) {

      // prevent page refresh on submit.
      event.preventDefault()

      fetch(`http://127.0.0.1:5000/needs/room_id?room_key=${tempRoomKey}`, {
                   method: 'GET',
                   headers: {
                     'Accept': 'application/json',
                     'Content-Type': 'application/json'
                   },
                 })
        .then(CheckError)
        .then(data => {

          const id = data['id']

          if (id > 0) {
            props.setRole(ROLE_PARTICIPANT)
            props.setRoom({key: tempRoomKey, id: id})
            setErrorText("")
          }
          else {
            setErrorText("Room Not Found")
          }
        });
    }

    return (
      <>
        <form onSubmit={handleSubmit}>
          <label>
            Room Key:
            <input type="text" value={tempRoomKey} onChange={handleChange} />
          </label>
          <input type="submit" value="Enter Room" />
        </form>
        <div>
          {errorText}
        </div>
      </>
    )
}

function RoomHeader(props) {

    return (
    <div>
      Room ID: {props.room.key}
    </div>
    )
}

function NeedsPicker(props) {

    return (
    <div>
      Select Needs
      {constants.needs.map(need => (
        <SelectableNeed
         key={need.need}
         need={need.need}
         room_id={props.room.id}
        />
      ))}
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

function SelectableNeed(props) {

  const [selected, setSelected] = useState(false);

  function addNeedToRoom(need) {

    // we only add a need once.
    if (!selected) {

      console.log(`Add need ${need}`)

      const need_data = {'room' : props.room_id, 'need': need}

      return fetch(`http://127.0.0.1:5000/needs/add_need`, {
                   method: 'POST',
                   headers: {
                     'Accept': 'application/json',
                     'Content-Type': 'application/json'
                   },
                   body: JSON.stringify(need_data)
                 })
        .then(CheckError)
        .then(setSelected(true));
    }
  }

  return (
    <button onClick={() => addNeedToRoom(props.need)}>
      {props.need}
    </button>
  )

}
