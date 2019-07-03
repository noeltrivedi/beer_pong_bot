// Import components
import React, { Component } from 'react';
import ReactTable from 'react-table';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import Select from 'react-select';

// Import .svg files:
import chomps_logo from './chomps_logo.svg';

// Import .css files:
import 'react-table/react-table.css'
import 'react-tabs/style/react-tabs.css';
import 'react-select/dist/react-select.css';
import './App.css';
import './fonts.css';




class App extends Component {

  /*
   * State for select boxes on team stats tab. 
   */
  state = {
    selectedOptionPlayer1: '',
    selectedOptionPlayer2: '',
  };

  /*
   * Handle change method for select boxes on team stats tab.
   */
  handleChangePlayer1 = (selectedOptionPlayer1) => {
    this.setState({ selectedOptionPlayer1 });
    // TODO, add lines in here to disable selected player's option on other dropdown menu. 
    if ({selectedOptionPlayer1} != null) { // Does not prevent crash because selectedOptionPlayer1.label is 
                                           // null upon canceling selection
      console.log(`Selected: ${selectedOptionPlayer1.label}`);
    }
  }

  handleChangePlayer2 = (selectedOptionPlayer2) => {
    this.setState({ selectedOptionPlayer2 });
    // TODO, add lines in here to disable selected player's option on other dropdown menu.  See other method.
    if ({selectedOptionPlayer2} != null) {
      console.log(`Selected: ${selectedOptionPlayer2.label}`);
    }
  }

  populatePlayerArray(names, data) {
    let numberOfPlayers = names.length;
    let i;
    for (i = 0; i < numberOfPlayers; i++) {
      let playerObject = {};
      playerObject['name'] = names[i];
      playerObject['totalCups'] = Math.random() * 150;
      playerObject['winPct'] = Math.random() * 100;
      let temp = Math.round(Math.random() * 100);
      playerObject['mostCommonPartner'] = names[temp % numberOfPlayers];
      playerObject['winsCarriedPct'] = Math.random() * 100;
      playerObject['winsWasCarriedPct'] = Math.random() * 100;
      playerObject['cupsPerGame'] = Math.random() * 10;
      playerObject['trolls'] = Math.round(Math.random() * 10) % 3;
      playerObject['totalBeersDrank'] = Math.random() * 100;
      playerObject['totalGameCount'] = Math.round(Math.random() * 100);
      playerObject['totalWinCount'] = Math.round(Math.random() * 100);
      playerObject['gameParticipationPct'] = Math.random() * 100;
      data.push(playerObject);
    }   
  }

  populateOptionsArray(names, options) {
    let numberOfPlayers = names.length;
    let i;
    for (i = 0; i < numberOfPlayers; i++) {
      let playerObject = {};
      playerObject['value'] = i;
      playerObject['label'] = names[i];
      playerObject['disabled'] = false;
      options.push(playerObject);
    }
  }

  render() {
  	// let data = [
	  	/*{
	  		name: 'Alan Coon',
	  		totalCups: 38,
	  		winPct: 44.44,
	  		mostCommonPartner: 'Noel Trivedi',
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
        totalCups: 38,
        winPct: 44.44,
        mostCommonPartner: 'Alan Coon',
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
        name: 'Jacob Karson',
        totalCups: 38,
        winPct: 44.44,
        mostCommonPartner: 'Mario Blanco',
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
        name: 'Mario Blanco',
        totalCups: 38,
        winPct: 44.44,
        mostCommonPartner: 'Jacob Karson',
        winsCarriedPct: 0.00,
        winsWasCarriedPct: 0.00,
        cupsPerGame: 4.22,
        trolls: 1,
        totalBeersDrank: 8.9,
        totalGameCount: 9,
        totalWinCount: 4,
        gameParticipationPct: 34.62,
      },*/
  	// ];

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

    let data = [], options = [];
    this.populatePlayerArray(names, data);
    this.populateOptionsArray(names, options);

    /*
     * We keep columns constant because the statistics we are tracking 
     * do not change during execution.  Used in the statistics spreadsheet tab.
     */ 

    /* let {nameColumnWidth} = 100;
     * let {winsWasCarriedPctColumnWidth} = 130;
     * let {totalWinCountColumnWidth} = 90;
     * let {gameCountColumnWidth} = 105;
     * let {cupsPerGameColumnWidth} = 75;
     * let {participationColumnWidth} = 80;
     */


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

    const { selectedOptionPlayer1 } = this.state;
    const { selectedOptionPlayer2 } = this.state;


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
            </TabPanel>
            <TabPanel class="App-tab-panel">
              <h2 className="App-tab-title">Team Statistics</h2>
              <h4 className="App-subtitle">Please select two players to see their team statistics.</h4>              
              <div className="App-tab-team-stats-row">
                <div className="App-tab-team-stats-column">          
                  <Select
                    name="player-1-input"
                    value={selectedOptionPlayer1}
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
                    value={selectedOptionPlayer2}
                    onChange={this.handleChangePlayer2}
                    options={options}
                  />
                </div>
              </div>
              <div>
                <p> {this.state['selectedOptionPlayer1'].label} </p>
                <p> {this.state['selectedOptionPlayer2'].label} </p>
              </div>
            </TabPanel>
            <TabPanel>
              <h2 className="App-tab-title">Season Statistics</h2>
              <h4 className="App-subtitle">Incase you degenerates were wondering how much you've collectively drank this semester.</h4>              
              <h3 className="App-tab-season-stats-key">Total Games:</h3>10
              <h3 className="App-tab-season-stats-key">Total Beers Drank:</h3>1 
              <h3 className="App-tab-season-stats-key">Total Cups Made:</h3>4
              <h3 className="App-tab-season-stats-key">Total Trolls:</h3>69
            </TabPanel>
            <TabPanel>
              <h2 className="App-tab-title">Visualizations</h2>
              <h4 className="App-subtitle">Feature coming soon, or not, I don't know dude.</h4>
            </TabPanel> 
          </Tabs>
  	    </div>
        <footer className="App-footer">
          <div className="App-footer-row">
            <div className="App-footer-column">
              <span><a href="https://github.com/noeltrivedi">@noeltrivedi</a></span>
            </div>
            <div className="App-footer-column">
              <span><a href="https://github.com/alancoon">@alancoon</a></span>
            </div>
          </div>
        </footer>
      </div>
    );
  }
}

export default App;
