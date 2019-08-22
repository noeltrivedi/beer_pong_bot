import React, {Component} from "react";
import ReactTable from "react-table";



export default class TableView extends Component {

    constructor(props) {
        super(props);
        this.state = {};
    }
      populatePlayerArray(names) {
        let data = [];
        for (let i = 0; i < names.length; i++) {
          let playerObject = {};
          playerObject["name"] = names[i];
          playerObject["totalCups"] = Math.random() * 150;
          playerObject["winPct"] = Math.random() * 100;
          let temp = Math.round(Math.random() * 100);
          playerObject["mostCommonPartner"] = names[temp % names.length];
          playerObject["winsCarriedPct"] = Math.random() * 100;
          playerObject["winsWasCarriedPct"] = Math.random() * 100;
          playerObject["cupsPerGame"] = Math.random() * 10;
          playerObject["trolls"] = Math.round(Math.random() * 10) % 3;
          playerObject["totalBeersDrank"] = Math.random() * 100;
          playerObject["totalGameCount"] = Math.round(Math.random() * 100);
          playerObject["totalWinCount"] = Math.round(Math.random() * 100);
          playerObject["gameParticipationPct"] = Math.random() * 100;
          data.push(playerObject);
        }
        return data;
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

          let data = this.populatePlayerArray(names);


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
                Cell: props => <span className='number'>{props.value}</span>
            },
            {
                Header: 'Win', // Win Percentage
                accessor: 'winPct',
                Cell: props => <span className='number'>{props.value}%</span> // Only want two decimal places, can be done on backend?
            },
            {
            /*
             * Changed mostCommonPartner to a string of the most common partner's name rather than an object.
             * Figured it's easier to do all of the calculation on the backend.
             */
                // id: 'mostCommonPartner', // Required because accessor is not a string
                Header: 'MCP', // Most Common Partner
                // accessor: d => d.mostCommonPartner.name, // Custom value accessor
            accessor: 'mostCommonPartner',
                Cell: props => <span className='string'><a href="">{props.value}</a></span>, // Link to most common partner profile
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
                    data={data}
                    columns={columns}
                    defaultPageSize={15}
                noDataText="No data yet, y'all better get drinkin'!"
                    className="-striped -highlight"
                />
          </div>
        );

    }
}