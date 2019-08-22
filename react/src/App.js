// Import components
import React, { Component } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import TableView from "./components/TableView";
import SeasonView from "./components/SeasonView";
import TeamsView from "./components/TeamsView";
import VisualizationsView from "./components/VisualizationsView";
import ChompsFooter from "./components/ChompsFooter";
// Import .svg files:
import chomps_logo from "./chomps_logo.svg";

// Import .css files:
import "react-table/react-table.css"
import "react-tabs/style/react-tabs.css";
import "react-select/dist/react-select.css";
import "./App.css";
import "./fonts.css";

export default class App extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
          <div className="App">
            <header className="App-header">
              <img src={chomps_logo} fill="white" className="App-logo svg" alt="logo" />
              <h1 className="App-title">Welcome to chomps.beer!</h1>
              <h4 className="App-subtitle">Your beer pong statistics hub for the twenty-first century.</h4>
            </header>
            <div className="App-body">
              <Tabs>
                <TabList>
                  <Tab>STATS</Tab>
                  <Tab>TEAMS</Tab>
                  <Tab>SEASON</Tab>
                  <Tab>VISUAL</Tab>
                </TabList>
                <TabPanel class="App-tab-panel">
                    <TableView/>
                </TabPanel>
                <TabPanel class="App-tab-panel">
                    <TeamsView/>
                </TabPanel>
                <TabPanel class="App-tab-panel">
                    <SeasonView/>
                </TabPanel>
                <TabPanel class="App-tab-panel">
                    <VisualizationsView/>
                </TabPanel>
              </Tabs>
            </div>
            <ChompsFooter/>
          </div>
        );
    }
  }

