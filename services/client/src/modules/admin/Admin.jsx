import React from 'react';
import {Route, Switch} from 'react-router-dom';
import {connect} from 'react-redux';

import {history} from 'helpers';
import {PrivateRoute} from 'modules/admin/routes/PrivateRoute';
import {LoginPage} from 'modules/admin/views/LoginPage/LoginPage';
import {AdminLayout} from "modules/admin/AdminLayout"
import authActions from "actions/auth.actions";
import {alertActions} from "actions/alert.actions";

import "modules/admin/assets/css/material-dashboard-react.css"

class Admin extends React.Component {
  constructor(props) {
    super(props);

    const {dispatch} = props;

    dispatch(authActions.checkLoggedIn());

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
    return this.props.checkedLoggedIn ? (
      <Switch>
        <Route path="/admin/login" component={LoginPage}/>
        <PrivateRoute
          loggedIn={this.props.loggedIn}
          path="/admin"
          component={AdminLayout}
          handleLogout={this.handleLogout}
        />
      </Switch>
    ) : null;
  }
}

function mapStateToProps(state) {
  const {auth} = state;
  return {
    loggedIn: auth.loggedIn,
    checkedLoggedIn: auth.checkedLoggedIn
  };
}

const connectedAdmin = connect(mapStateToProps)(Admin);
export {connectedAdmin as Admin};