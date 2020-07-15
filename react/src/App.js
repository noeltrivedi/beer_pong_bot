// Import components
import React, { Component } from "react";
import axios from "axios";
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


function handleError(error) {
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
    } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);
    } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
    }
    console.log(error.config);
}


export default class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            names: [],
            season: {}
        };
    }

    componentDidMount() {
        let body = {};
        axios
            .post("/api/context", body)
            .then(res => {
                this.setState({
                    names: res.data.names,
                    season: res.data.season
                });
            })
            .catch(err => { handleError(err); });
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <img src={chomps_logo} fill="white" className="App-logo svg" alt="logo" />
                    <h1 className="App-title">Welcome to Web Chomps</h1>
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
                            <TableView names={this.state.names} season={this.state.season}/>
                        </TabPanel>
                        <TabPanel class="App-tab-panel">
                            <TeamsView names={this.state.names}/>
                        </TabPanel>
                        <TabPanel class="App-tab-panel">
                            <SeasonView season={this.state.season}/>
                        </TabPanel>
                        <TabPanel class="App-tab-panel">
                            <VisualizationsView names={this.state.names}/>
                        </TabPanel>
                    </Tabs>
                </div>
                <ChompsFooter/>
            </div>
        );
    }
}

