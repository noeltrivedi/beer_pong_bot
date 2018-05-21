import React, { Component } from 'react';
import ReactTable from "react-table";

// Import .svg files:
import chomps_logo from './chomps_logo.svg';

// Import .css files:
import './App.css';
import './fonts.css';
import 'react-table/react-table.css'


class App extends Component {
  render(PlayerData) {
  	var data = [
	  	{
	  		name: 'Alan Coon',
	  		totalCups: 21,
	  		winPct: 44.24,
	  		mostCommonPartner: {
	  			name: 'Noel Trivedi',
	  			totalCups: 22,
	  		}

	  	},
	  	{
	  		name: 'Noel Trivedi',
	  		totalCups: 22,
	  		mostCommonPartner: {
	  			name: 'Alan Coon',
	  			totalCups: 21
	  		}
	  	},
  	];

  	console.log(PlayerData);

  	var i;
  	var numberOfPlayers = 5;
  	for (i = 0; i < numberOfPlayers; i++) {
  		var playerObject = {};
  		playerObject['name'] = 'Hello' + i;
  		playerObject['mostCommonPartner'] = { name: 'None' };
  		data.push(playerObject);
  	}

  	const columns = [
  		{
  			Header: 'Name',
  			accessor: 'name', // String-based value accessor
  			Cell: props => <span className='string'><a href="">{props.value}</a></span> // Link to player profile
  		},
  		{
  			Header: 'Total Cups',
  			accessor: 'totalCups',
  			Cell: props => <span className='number'>{props.value}</span> // Custom cell components
  		},
  		{
  			Header: 'Win', // Win Percentage
  			accessor: 'winPct',
  			Cell: props => <span className='number'>{props.value}%</span> // Only want two decimal places, can be done on backend?
  		},
  		{
  			id: 'mostCommonPartner', // Required because accessor is not a string
  			Header: 'MCP', // Most Common Partner
  			accessor: d => d.mostCommonPartner.name, // Custom value accessor
  			Cell: props => <span className='string'><a href="">{props.value}</a></span> // Link to most common partner profile
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
  			width: 130 // Set width of column otherwise header name gets cut off
  		},
  		{
  			Header: 'CPG', // Cups per Game
  			accessor: 'cupsPerGame',
  			Cell: props => <span className='number'>{props.value}</span>, // Only want two decimal places, can be done on backend?
  			width: 75 // Narrow stat, save space for other columns
  		},
  		{
  			Header: 'Times Trolled',
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
  			Cell: props => <span className='number'>{props.value}</span>
  		},
  		{
  			Header: 'Game Count',
  			accessor: 'totalGameCount',
  			Cell: props => <span className='number'>{props.value}</span>
  		}
  	];

    return (
      <div className="App">
    	<header className="App-header">
          <img src={chomps_logo} className="App-logo" alt="logo" />
          <h1 className="App-title">welcome to chomps.beer</h1>
          <h4 className="App-subtitle">your beer pong statistics hub for the twenty-first century</h4>
        </header>
        <div className="App-body">
			<ReactTable
				data={data}
				columns={columns}
				defaultPageSize={15}
	          	noDataText="No data yet, y'all better get drinkin'!"
				className="-striped -highlight"
			/>
        	<br />
	    </div>
      </div>
    );

  }
}

export default App;
