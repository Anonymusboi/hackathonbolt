import React, {Component} from "react";
import {createRoot} from "react-dom/client" ;
import HomePage from "./HomePage.js";

export default class App extends Component {
    constructor (props){
        super(props);
    }

    render() {
        return (
            <div>
                <HomePage />  {/* Home page and routing information */}
            </div>
        );
    }

}

const appDiv = document.getElementById("app");
const root = createRoot(appDiv);
root.render(<App />);