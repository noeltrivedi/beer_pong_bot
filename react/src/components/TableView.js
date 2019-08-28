import React, {Component} from "react";
import axios from "axios";
import ReactTable from "react-table";
import "../react-sticky-table.css";

export default class TableView extends Component {

    constructor(props) {
        super(props);
        this.state = {
            playerData: {}
        };
        this.loadPlayerData();
    }

    loadPlayerData = () => {
        let body = {};
        axios
            .post("/api/table", body)
            .then(res => {
                console.log("Player Data:", res.data);
                this.setState({ playerData: res.data });
            })
            .catch(err => {
                console.log(err);
            });
    };

    cleanTableValue = (value, significantFigures) => {
        if (isNaN(value)) {
            return 0;
        } else if (value % 1 > 0) {
            return value.toFixed(significantFigures);
        } else return value;
    }

    populatePlayerArray() {
        let data = [];
        for (let playerName in this.state.playerData) {
            let playerData = this.state.playerData[playerName];
            let playerObject = {};
            playerObject["name"] = playerName;
            playerObject["totalCups"] = playerData["cups"];
            playerObject["winPct"] = this.cleanTableValue(playerData["wins"] / playerData["games"] * 100, 3);
            playerObject["mostCommonPartner"] = playerData["mcp"];
            playerObject["winsCarriedPct"] = this.cleanTableValue(playerData["carryRate"], 3);
            playerObject["winsWasCarriedPct"] = this.cleanTableValue(playerData["carriedRate"], 3);
            playerObject["cupsPerGame"] = this.cleanTableValue(playerData["cups"] / playerData["games"], 3);
            playerObject["trolls"] = playerData["trolls"];
            playerObject["totalBeersDrank"] = this.cleanTableValue(playerData["beers"], 1);
            playerObject["totalGameCount"] = playerData["games"];
            playerObject["totalWinCount"] = playerData["wins"];
            if (this.props.season) {
                let totalGames = this.props.season.games;
                playerObject["gameParticipationPct"] = this.cleanTableValue(playerData["games"] / totalGames * 100, 3);
            } else {
                playerObject["gameParticipationPct"] = "...";
            }
            data.push(playerObject);
        }
        return data;
    }

    render() {
        let data = this.populatePlayerArray();


        const columns = [
            {
                Header: 'Name',
                accessor: 'name', // String-based value accessor
                Cell: props => <span className='string'><a href="">{props.value}</a></span>, // Link to player profile
                // width: {nameColumnWidth}
            },
            {
                Header: 'Total Cups',
                accessor: 'totalCups',
                Cell: props => <span className='number'>{props.value}</span>,
            },
            {
                Header: 'Win', // Win Percentage
                accessor: 'winPct',
                Cell: props => <span className='number'>{props.value}%</span> // Only want two decimal places, can be done on backend?
            },
            {
                Header: 'MCP', // Most Common Partner
                accessor: 'mostCommonPartner',
                // Cell: props => <span className='string'><a href="">{props.value}</a></span>, // Link to most common partner profile
                Cell: props => <span className='string'>{props.value}</span>, // No link for now
                // width: {nameColumnWidth}
            },
            {
                Header: 'Carried', // Wins Carried Percentage
                accessor: 'winsCarriedPct',
                Cell: props => <span className='number'>{props.value}%</span> // Only want two decimal places, can be done on backend?
            },
            {
                Header: 'Was Carried', // Wins Was Carried Percentage
                accessor: 'winsWasCarriedPct',
                Cell: props => <span className='number'>{props.value}%</span>, // Only want two decimal places, can be done on backend?
                // width: {winsWasCarriedPctColumnWidth} // Set width of column otherwise header name gets cut off
            },
            {
                Header: 'CPG', // Cups per Game
                accessor: 'cupsPerGame',
                Cell: props => <span className='number'>{props.value}</span>, // Only want two decimal places, can be done on backend?
                // width: {cupsPerGameColumnWidth} // Narrow stat, save space for other columns
            },
            {
                Header: 'Trolls',
                accessor: 'trolls',
                Cell: props => <span className='number'>{props.value}</span>
            },
            {
                Header: 'Beers Drank',
                accessor: 'totalBeersDrank',
                Cell: props => <span className='number'>{props.value}</span>
            },
            {
                Header: 'Win Count',
                accessor: 'totalWinCount',
                Cell: props => <span className='number'>{props.value}</span>,
                // width: {totalWinCountColumnWidth}
            },
            {
                Header: 'Game Count',
                accessor: 'totalGameCount',
                Cell: props => <span className='number'>{props.value}</span>
            },
            {
                Header: 'Participation',
                accessor: 'gameParticipationPct',
                Cell: props => <span className='number'>{props.value}%</span>,
                // width: {participationColumnWidth}
            }
        ];

        return (
            <div className="App-tab">
                <h2 className="App-tab-title">Statistics Spreadsheet</h2>
                <h4 className="App-subtitle">Click on a column header to sort.</h4>
                <ReactTable
                    // stickyColumnCount={0}
                    data={data}
                    columns={columns}
                    defaultPageSize={20}
                    defaultSorted={[{
                            id: "totalCups",
                            desc: true
                    }]}
                    noDataText="No data yet. Go play some pong, pledge."
                    className="-striped -highlight"
                />
            </div>
        );

    }
}