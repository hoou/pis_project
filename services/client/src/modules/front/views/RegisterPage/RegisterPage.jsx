import React from "react"
import {Grid, Paper, Typography, withStyles} from "material-ui";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";
import RegisterForm from "modules/front/forms/RegisterForm";
import authActions from "../../../../actions/auth.actions";

const styles = {
  page: {
    padding: 50
  }
};

class RegisterPage extends React.Component {
  submit = values => {
    const {dispatch} = this.props;

    dispatch(authActions.register(values["email"], values["password"]));
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
                <Typography variant="headline">Registration</Typography>
                <RegisterForm onSubmit={this.submit}/>
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

export default connect(mapStateToProps)(withStyles(styles)(RegisterPage))