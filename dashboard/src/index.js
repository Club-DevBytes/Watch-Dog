import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";


import { BrowserRouter, Route, Switch } from "react-router-dom";

// import { Attendence, Intruder, Suspicious } from "./Pages";

import Attendence from "./Pages/Attendence";
import Unregistered from "./Pages/Unregistered";
import Suspicious from "./Pages/Suspicious";

const Root = () => (
    <BrowserRouter>
      <div className="allcontainer">
        <Switch>
        <Route exact path="/suspicious" component={Suspicious} />
          <Route exact path="/unregistered" component={Unregistered} />
          <Route exact path="/" component={Attendence} />
          <Route component={Error} />
        </Switch>
      </div>
    </BrowserRouter>
);

ReactDOM.render(<Root />, document.getElementById("root"));

serviceWorker.unregister();