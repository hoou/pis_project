import React from 'react';
import {Router, Route, Switch} from 'react-router-dom';
import {connect} from 'react-redux';

import {history} from 'helpers';
import {Admin} from "modules/admin/Admin"
import {alertActions} from "actions/alert.actions";
import Front from "modules/front/Front";

class App extends React.Component {
  constructor(props) {
    super(props);

    const {dispatch} = props;

    history.listen((location, action) => {
      // clear alert on location change
      dispatch(alertActions.clear());
    });
  }

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

const connectedApp = connect()(App);
export {connectedApp as App};