import React, {Component} from "react";
import FontAwesomeIcon from "@fortawesome/react-fontawesome";
export default class RefreshButton extends Component {
    constructor(props) {
        super(props);
        this.state = {
            refreshing: false
        };
    }

    render() {
        let icon = this.state.refreshing ?
        return (
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
        );
    }
}