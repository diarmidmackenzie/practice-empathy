import React from "react";
import { useState } from "react";
import { QueryClient, QueryClientProvider } from 'react-query'
import { ReactQueryDevtools } from 'react-query/devtools'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { CollaborateTab } from './Collaborate/Collaborate';
import 'react-tabs/style/react-tabs.css';

const queryClient = new QueryClient()


function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
          <NVCApp/>
      </div>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

function NVCApp() {

  /* Collaboration state tthat we want to maintain when switching tabs is kept
     at this level */
  const [collaborationRoom, setCollaborationRoom] = useState("");
  const [collaborationRole, setCollaborationRole] = useState(0);

    return (
      <>
        <Tabs>
          <TabList>
            <Tab>Home</Tab>
            <Tab>Collaborate</Tab>
            <Tab>Practice</Tab>
            <Tab>Tutorial</Tab>
            <Tab>About</Tab>
            <Tab>FAQ</Tab>
            <Tab>Help Us</Tab>
          </TabList>
          <TabPanel>
          </TabPanel>
          <TabPanel>
            <CollaborateTab
             room = {collaborationRoom}
             role = {collaborationRole}
             setRoom = {setCollaborationRoom}
             setRole = {setCollaborationRole}/>
          </TabPanel>
          <TabPanel>
          </TabPanel>
          <TabPanel>
          </TabPanel>
          <TabPanel>
          </TabPanel>
          <TabPanel>
          </TabPanel>
          <TabPanel>
          </TabPanel>
        </Tabs>
      </>
  );
}

export default App;
