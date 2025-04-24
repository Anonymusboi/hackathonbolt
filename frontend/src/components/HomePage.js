import React, { Component } from "react";
import AccountCreationPage from "./AccountCreationPage.js";
import { BrowserRouter as Router, Routes, Route, Link, redirect } from "react-router-dom";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }

    render() { 
        return (<Router>
            <Routes>
            <Route path="/home" element={<p>Home page</p>} /> {/* Home page */}
                    <Route path="/account-creation" element={<AccountCreationPage />} /> {/* Account creation page */}
                    <Route exact path="/" element={<p>Default</p>} /> {/* Default route */}
                    <Route path="*" element={<p>404 Not Found</p>} /> {/* Catch-all route for 404 */}
            </Routes>
        </Router>
        );
    }
}