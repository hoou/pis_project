import React from "react";
import {Paper} from "material-ui";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";

class ProfilePage extends React.Component {
  render() {
    const {loggedIn, checkedLoggedIn} = this.props;

    return (
      checkedLoggedIn && (
        loggedIn ? (
          <Paper>
            "secret stuff"
          </Paper>
        ) : (
          <Redirect to="/login"/>
        )
      )
    );
  }
}

const mapStateToProps = state => ({
  loggedIn: state.auth.loggedIn,
  checkedLoggedIn: state.auth.checkedLoggedIn
});
export default connect(mapStateToProps)(ProfilePage);