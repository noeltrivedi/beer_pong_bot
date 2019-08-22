import React, {Component} from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import Select from "react-select";

export default class TeamsView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            selectedOptionPlayer1: null,
            selectedOptionPlayer2: null,
        };
    }
      /**
       * Handle change method for select boxes on team stats tab.
       */
      handleChangePlayer1 = (selectedOptionPlayer1) => {
        this.setState({ selectedOptionPlayer1: selectedOptionPlayer1 });
        // TODO, add lines in here to disable selected player's option on other dropdown menu.
        if ({selectedOptionPlayer1} != null) { // Does not prevent crash because selectedOptionPlayer1.label is
                                               // null upon canceling selection
          console.log(`Selected: ${selectedOptionPlayer1.label}`);
        }
      }

      handleChangePlayer2 = (selectedOptionPlayer2) => {
        this.setState({ selectedOptionPlayer2: selectedOptionPlayer2 });
        // TODO, add lines in here to disable selected player"s option on other dropdown menu.  See other method.
        if ({selectedOptionPlayer2} != null) {
          console.log(`Selected: ${selectedOptionPlayer2.label}`);
        }
      }

      populateOptionsArray(names) {
        let options = [];
        for (let i = 0; i < names.length; i++) {
          let playerObject = {};
          playerObject["value"] = i;
          playerObject["label"] = names[i];
          playerObject["disabled"] = false;
          options.push(playerObject);
        }
        return options;
      }


    render() {
            let names = [
          'Alan Coon',
          'Noel Trivedi',
          'Jacob Karson',
          'Michael Spielberg',
          'Landon Fadel',
          'Joshua Pollard',
          'Mario Blanco',
          'Danyal Brink',
          'Ben Kraus',
          'Baylee Jones',
          'Pledge Jerry Hernandez',
          'Julian Garcia',
          'Aaron Licon',
          'Mario Portillo',
          'Chris Cain',
          'Dennis Naroditskiy',
          'Niraj Mehta',
          'Andrew Heerman',
          'Jonathan Santana',
          'Zachary Anziano',
          'Ali Espinoza',
          'Sam Hanoura',
        ];
        let options = this.populateOptionsArray(names, options);
        return (
            <div>
              <h2 className="App-tab-title">Team Statistics</h2>
              <h4 className="App-subtitle">Please select two players to see their team statistics.</h4>
              <div className="App-tab-team-stats-row">
                <div className="App-tab-team-stats-column">
                  <Select
                    name="player-1-input"
                    value={this.state.selectedOptionPlayer1}
                    onChange={this.handleChangePlayer1}
                    /*
                     * TODO: You want to use a complete list of all nicknames
                     * as the options here.  Either that or canonical names, but nicknames
                     * included would be better.
                     */
                    options={options}
                  />
                </div>
                <div className="App-tab-team-stats-column">
                  <Select
                    name="player-2-input"
                    value={this.state.selectedOptionPlayer2}
                    onChange={this.handleChangePlayer2}
                    options={options}
                  />
                </div>
              </div>
              <div>
                <p> {this.state.selectedOptionPlayer1 ? this.state.selectedOptionPlayer1.label : null} </p>
                <p> {this.state.selectedOptionPlayer2 ? this.state.selectedOptionPlayer2.label : null} </p>
              </div>
            </div>
        );
    }
}

