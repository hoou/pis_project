import React from 'react';
import {Router, Route, Switch} from 'react-router-dom';
import {connect} from 'react-redux';

import {history} from 'helpers';
import {PrivateRoute} from 'routes/PrivateRoute';
import {LoginPage} from 'views/LoginPage';
import Admin from "containers/Admin/Admin"
import authActions from "actions/auth.actions";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.props.dispatch(authActions.status());

    this.handleLogout = this.handleLogout.bind(this);
  }

  handleLogout() {
    console.log("handle logout", this.props);
    this.props.dispatch(authActions.logout())
  }

  render() {
    return this.props.checkedStatus ? (
      <div className="jumbotron">
        <div className="container">
          <div className="col-sm-8 col-sm-offset-2">
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
          </div>
        </div>
      </div>
    ) : (<div/>);
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