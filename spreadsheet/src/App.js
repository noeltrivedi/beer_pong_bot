import React, { Component } from 'react';
import ReactTable from "react-table";

// Import .svg files:
import logo from './logo.svg';
import chomps_logo from './chomps_logo.svg';

// Import .css files:
import './App.css';
import './fonts.css';
import 'react-table/react-table.css'


class App extends Component {
  render() {
  	const data = [
	  	{
	  		name: 'Alan Coon',
	  		totalCups: 21,
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
  	]

  	const columns = [
  		{
  			Header: 'Name',
  			accessor: 'name' // String-based value accessor
  		},
  		{
  			Header: 'Total Cups',
  			accessor: 'totalCups',
  			Cell: props => <span className='number'>{props.value}</span> // Custom cell components
  		},
  		{
  			Header: 'Win %', // Win Percentage
  			accessor: 'winPct',
  			Cell: props => <span className='number'>{props.value}</span> // TODO, make sure class supports double type
  		},
  		{
  			id: 'mostCommonPartner', // Required because accessor is not a string
  			Header: 'MCP', // Most Common Partner
  			accessor: d => d.mostCommonPartner.name // Custom value accessor
  		},
  		{
  			Header: 'Carried %', // Wins Carried Percentage
  			accessor: 'winsCarriedPct',
  			Cell: props => <span className='number'>{props.value}</span> // TODO, make sure class supports double type
  		},
  		{
  			Header: 'Was Carried %', // Wins Was Carried Percentage
  			accessor: 'winsWasCarriedPct',
  			Cell: props => <span className='number'>{props.value}</span> // TODO, make sure class supports double type
  		},
  		{
  			Header: 'Cups/Game', // Cups per Game
  			accessor: 'cupsPerGame',
  			Cell: props => <span className='number'>{props.value}</span> // TODO, make sure class supports double type
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
  	]

    return (
      <div className="App">
    	<header className="App-header">
          <img src={chomps_logo} className="App-logo" alt="logo" />
          <h1 className="App-title">welcome to chomps.beer</h1>
          <h4 className="App-subtitle">your beer pong statistics hub for the twenty-first century</h4>
        </header>
        <div className="body">
			<ReactTable
				data={data}
				columns={columns}
				defaultPageSize={30}
				className="-striped -highlight"
			/>
	    </div>
      </div>
    );

  }
}

export default App;
