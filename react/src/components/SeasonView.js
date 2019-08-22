import React, {Component} from "react";
import { TabPanel } from "react-tabs";

export default class SeasonView extends Component {

    constructor(props) {
        super(props);
        this.state = {
        };
    }

    async componentDidMount() {

    }


    render() {
        return (
            <div>
              <h2 className="App-tab-title">Season Statistics</h2>
              <h4 className="App-subtitle">Incase you degenerates were wondering how much you've collectively drank this semester.</h4>
              <h3 className="App-tab-season-stats-key">Total Games:</h3>10
              <h3 className="App-tab-season-stats-key">Total Beers Drank:</h3>1
              <h3 className="App-tab-season-stats-key">Total Cups Made:</h3>4
              <h3 className="App-tab-season-stats-key">Total Trolls:</h3>69
            </div>
        );
    }
}



