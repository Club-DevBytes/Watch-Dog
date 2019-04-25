import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';


import Attendence from "./Pages/Unregistered"

class App extends Component {
  render() {
    return (
      <div className="App">
        <Attendence/>
      </div>
    );
  }
}

export default App;
