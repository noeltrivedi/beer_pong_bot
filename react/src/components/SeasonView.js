import React, {Component} from "react";

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
            <div className="App-tab-season-stats-key">
                <h2 className="App-tab-title">Season Statistics</h2>
                <h4 className="App-subtitle">Incase you degenerates were wondering how much you've collectively drank this semester.</h4>
                <h3 className="App-tab-season-stats-key">Total Games:</h3>{this.props.season.games}
                <h3 className="App-tab-season-stats-key">Total Beers Drank:</h3>{this.props.season.beers}
                <h3 className="App-tab-season-stats-key">Total Cups Made:</h3>{this.props.season.cups}
                <h3 className="App-tab-season-stats-key">Total Trolls:</h3>{this.props.season.trolls}
                <br/>
                <br/>
            </div>
        );
    }
}



