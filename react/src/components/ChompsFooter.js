import React, {Component} from "react";

export default class ChompsFooter extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <footer className="App-footer">
              <div className="App-footer-row row">
                <div className="App-footer-column col-sm-5">
                  <span><a href="https://github.com/noeltrivedi">@noeltrivedi</a></span>
                </div>
                <div className="App-footer-column col-sm-5">
                  <span><a href="https://github.com/alancoon">@alancoon</a></span>
                </div>
              </div>
            </footer>
        );
    }
}