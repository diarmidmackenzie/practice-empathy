import React from "react";
//import { useState } from "react";
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { CollaborateTab } from './Collaborate/Collaborate';
import 'react-tabs/style/react-tabs.css';

function App() {
  return (
    <div className="App">
        <NVCApp/>
    </div>
  );
}

function NVCApp() {

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
            <CollaborateTab/>
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
