import React, {Component} from "react";
import Select from "react-select";
import { Button } from "reactstrap";
import axios from "axios";


export default class TeamsView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            selectedOptionPlayer1: null,
            selectedOptionPlayer2: null,
            teamData: null,
            message: "",
        };
    }

    /**
     * Handle change method for select boxes on team stats tab.
     */
    handleChangePlayer1 = (selectedOptionPlayer1) => {
        this.setState({ selectedOptionPlayer1: selectedOptionPlayer1, teamData: null });
    };

    handleChangePlayer2 = (selectedOptionPlayer2) => {
        this.setState({ selectedOptionPlayer2: selectedOptionPlayer2, teamData: null });
    };

    populateOptionsArray1 = () => {
        let options = [];
        for (let i = 0; i < this.props.names.length; i++) {
            let playerObject = {};
            playerObject["value"] = i;
            playerObject["label"] = this.props.names[i];
            if (this.state.selectedOptionPlayer2) {
                playerObject["disabled"] = this.state.selectedOptionPlayer2.value === i;
            } else {
                playerObject["disabled"] = false;
            }
            options.push(playerObject);
        }
        return options;
    };

    populateOptionsArray2 = () => {
        let options = [];
        for (let i = 0; i < this.props.names.length; i++) {
            let playerObject = {};
            playerObject["value"] = i;
            playerObject["label"] = this.props.names[i];
            if (this.state.selectedOptionPlayer1) {
                playerObject["disabled"] = this.state.selectedOptionPlayer1.value === i;
            } else {
                playerObject["disabled"] = false;
            }
            options.push(playerObject);
        }
        return options;
    };

    handleSubmit = () => {
        return new Promise((resolve, reject) => {
            if (!this.state.selectedOptionPlayer1 || !this.state.selectedOptionPlayer2) {
                this.setState({ message: "Please select two players." });
                reject();
            }
            let body = {
                'player1': this.state.selectedOptionPlayer1.label,
                'player2': this.state.selectedOptionPlayer2.label,
            };
            axios
                .post("/api/teams", body)
                .then(res => {
                    console.log(res.data);
                    if (res.data.error) {
                        this.setState({ message: res.data.message, teamData: null });
                    } else {
                        this.setState({ message: "", teamData: res.data });
                    }
                    resolve();
                })
                .catch(err => {
                    console.log(err);
                    reject();
                });
        });
    };

    renderAlert = () => {
        if (this.state.message.length) {
            return (
                <div className="alert alert-danger">
                    {this.state.message}
                </div>
            );
        } else {
            return null;
        }
    };

    renderStats = () => {
        if (this.state.teamData) {
            return (
                <div>
                    <h3>{this.state.selectedOptionPlayer1.label}</h3>
                    <h5>Cups per Game</h5>
                    {this.state.teamData.player1.cpg}
                    <h5>Carry Percentage</h5>
                    {this.state.teamData.player1.carryPct}%
                    <hr/>
                    <h3>{this.state.selectedOptionPlayer2.label}</h3>
                    <h5>Cups per Game</h5>
                    {this.state.teamData.player2.cpg}
                    <h5>Carry Percentage</h5>
                    {this.state.teamData.player2.carryPct}%
                    <hr/>
                    <h5>Games Played</h5>
                    {this.state.teamData.games}
                    <h5>Cups Made</h5>
                    {this.state.teamData.cupsLeft}
                    <h5>Win Percentage</h5>
                    {this.state.teamData.winPct}%
                </div>
            );
        } else {
            return null;
        }
    };

    render() {
        let options1 = this.populateOptionsArray1();
        let options2 = this.populateOptionsArray2();
        return (
            <div>
                <h2 className="App-tab-title">Team Statistics</h2>
                <h4 className="App-subtitle">Please select two players to see their team statistics.</h4>
                <div className="teams-view-row row">
                    <div className="teams-view-col col">
                        {this.renderAlert()}
                    </div>
                </div>
                <div className="teams-view-row row">
                    <div className="teams-view-col col-sm-6">
                        <Select
                            name="player-1-input"
                            value={this.state.selectedOptionPlayer1}
                            onChange={this.handleChangePlayer1}
                            options={options1}
                        />
                    </div>
                    <div className="teams-view-col col-sm-6">
                        <Select
                            name="player-2-input"
                            value={this.state.selectedOptionPlayer2}
                            onChange={this.handleChangePlayer2}
                            options={options2}
                        />
                    </div>
                </div>
                <div className="teams-view-row row">
                    <div className="col-sm-12">
                        <Button color="secondary" className="btn-block" onClick={this.handleSubmit}>
                            Get Stats
                        </Button>
                    </div>
                </div>
                <div className="teams-view-row row">
                    <div className="teams-view-col col">
                        {this.renderStats()}
                    </div>
                </div>
            </div>
        );
    }
}

