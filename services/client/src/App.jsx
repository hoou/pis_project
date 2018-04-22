import React from 'react';
import {Router, Route, Switch} from 'react-router-dom';

import {history} from 'helpers';
import {Admin} from "modules/admin/Admin"
import Front from "modules/front/Front";

export class App extends React.Component {
  render() {
    return (
      <Router history={history}>
        <Switch>
          <Route path="/admin" component={Admin}/>
          <Route path="/" component={Front}/>
        </Switch>
      </Router>
    )
  }
}
