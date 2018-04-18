import React from 'react';
import {Router, Route, Switch} from 'react-router-dom';
import {connect} from 'react-redux';

import {history} from 'helpers';
import {PrivateRoute} from 'routes/PrivateRoute';
import {LoginPage} from 'views/LoginPage/LoginPage';
import {Admin} from "containers/Admin/Admin"
import authActions from "actions/auth.actions";
import {alertActions} from "actions/alert.actions";

class App extends React.Component {
  constructor(props) {
    super(props);

    const {dispatch} = props;

    dispatch(authActions.status());

    this.handleLogout = this.handleLogout.bind(this);

    history.listen((location, action) => {
      // clear alert on location change
      dispatch(alertActions.clear());
    });
  }

  handleLogout() {
    this.props.dispatch(authActions.logout())
  }

  render() {
    return this.props.checkedStatus ? (
      <Router history={history}>
        <Switch>
          <Route exact path="/login" component={LoginPage}/>
          <PrivateRoute
            loggedIn={this.props.loggedIn}
            path="/"
            component={Admin}
            handleLogout={this.handleLogout}
          />
        </Switch>
      </Router>
    ) : null;
  }
}

function mapStateToProps(state) {
  const {auth} = state;
  return {
    loggedIn: auth.loggedIn,
    checkedStatus: auth.checkedStatus
  };
}

const connectedApp = connect(mapStateToProps)(App);
export {connectedApp as App};