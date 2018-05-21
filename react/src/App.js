// Import components
import React, { Component } from 'react';
import ReactTable from 'react-table';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';

// Import .svg files:
import chomps_logo from './chomps_logo.svg';

// Import .css files:
import 'react-table/react-table.css'
import 'react-tabs/style/react-tabs.css';
import './App.css';
import './fonts.css';




class App extends Component {
  render(PlayerData) {
  	var data = [
	  	{
	  		name: 'Alan Coon',
	  		totalCups: 38,
	  		winPct: 44.44,
	  		mostCommonPartner: {
	  			name: 'Noel Trivedi',
	  			totalCups: 22,
	  		},
        winsCarriedPct: 0.00,
        winsWasCarriedPct: 0.00,
        cupsPerGame: 4.22,
        trolls: 0,
        totalBeersDrank: 8.9,
        totalGameCount: 9,
        totalWinCount: 4,
        gameParticipationPct: 34.62,



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
      playerObject['totalCups'] = 0;
      playerObject['winPct'] = 0.00;
      playerObject['mostCommonPartner'] = { name: 'None' };
      playerObject['winsCarriedPct'] = 0.00;
      playerObject['winsWasCarriedPct'] = 0.00;
      playerObject['cupsPerGame'] = 0.00;
      playerObject['trolls'] = 0;
      playerObject['totalBeersDrank'] = 0;
      playerObject['totalGameCount'] = 0;
      playerObject['totalWinCount'] = 0;
      playerObject['gameParticipationPct'] = 0.00;
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
  			Cell: props => <span className='number'>{props.value}</span>
  		},
  		{
  			Header: 'Game Count',
  			accessor: 'totalGameCount',
  			Cell: props => <span className='number'>{props.value}</span>
  		},
      {
        Header: 'Game Participation',
        accessor: 'gameParticipationPct',
        Cell: props => <span className='number'>{props.value}%</span>,
        width: 150
      }
  	];

    return (
      <div className="App">
      	<header className="App-header">
          <img src={chomps_logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to chomps.beer!</h1>
          <h4 className="App-subtitle">Your beer pong statistics hub for the twenty-first century.</h4>
        </header>   
        <div className="App-body">
          <Tabs>
            <TabList>
              <Tab>STATS</Tab>
              <Tab>TEAMS</Tab>
              <Tab>SEASON</Tab> 
            </TabList>
            <TabPanel>
              <div className="App-tab">
                <h2 className="App-tab-title">Statistics Spreadsheet</h2>
          			<ReactTable
          				data={data}
          				columns={columns}
          				defaultPageSize={15}
          	          	noDataText="No data yet, y'all better get drinkin'!"
          				className="-striped -highlight"
          			/>
              </div>
            </TabPanel>
            <TabPanel>
              <h2 className="App-tab-title">Team Statistics</h2>
              <h4 className="App-subtitle">Please select two players to see their team statistics.</h4>              
            </TabPanel>
            <TabPanel>
              <h2 className="App-tab-title">Season Statistics</h2>
              <h3 className="App-tab-season-stats-key">Total Games:</h3>
              <h3 className="App-tab-season-stats-key">Total Beers Drank:</h3> 
              <h3 className="App-tab-season-stats-key">Total Cups Made:</h3>
              <h3 className="App-tab-season-stats-key">Total Trolls:</h3>
            </TabPanel>
          </Tabs>
  	    </div>
      </div>
    );

  }
}

export default App;
