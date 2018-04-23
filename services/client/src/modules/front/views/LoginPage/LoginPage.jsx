import React from "react"
import {Grid, Paper, Typography, withStyles} from "material-ui";
import LoginForm from "modules/front/forms/LoginForm";
import authActions from "actions/auth.actions";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";

const styles = {
  page: {
    padding: 50
  }
};

class LoginPage extends React.Component {
  submit = values => {
    const {dispatch} = this.props;
    dispatch(authActions.login(values.email, values.password, false))
  };

  render() {
    const {classes, checkedLoggedIn, loggedIn} = this.props;

    return (
      checkedLoggedIn && (
        loggedIn ? (
          <Redirect to="/home"/>
        ) : (
          <Grid container justify="center">
            <Grid item xs={12} sm={6} md={4} lg={3}>
              <Paper className={classes.page}>
                <Typography variant="headline">Please, log in</Typography>
                <LoginForm onSubmit={this.submit}/>
              </Paper>
            </Grid>
          </Grid>
        )
      )
    )
  }
}

const mapStateToProps = state => ({
  checkedLoggedIn: state.auth.checkedLoggedIn,
  loggedIn: state.auth.loggedIn
});

export default connect(mapStateToProps)(withStyles(styles)(LoginPage))