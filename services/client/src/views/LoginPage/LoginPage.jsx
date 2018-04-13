import React from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import authActions from 'actions/auth.actions';
import LoginForm from "forms/LoginForm/LoginForm";
import {Redirect} from "react-router-dom";
import {Button, Grid, withStyles} from "material-ui";
import ItemGrid from "components/Grid/ItemGrid";
import RegularCard from "../../components/Cards/RegularCard";
import SnackbarContent from "../../components/Snackbar/SnackbarContent";

const styles = theme => ({
  root: {
    flexGrow: 1,
    marginTop: 50
  },
  formGridCntainer: {
    padding: 10
  },
  paper: {
    height: 140,
    width: 100,
  },
  control: {
    padding: theme.spacing.unit * 2,
  },
});


class LoginPage extends React.Component {

  constructor(props) {
    super(props);

    // reset login status
    // this.props.dispatch(authActions.logout());

    // this.state = {
    // 	email: '',
    // 	password: '',
    // 	submitted: false
    // };

    // this.handleChange = this.handleChange.bind(this);
    // this.handleSubmit = this.handleSubmit.bind(this);
  }

  // handleChange(e) {
  // 	const {name, value} = e.target;
  // 	this.setState({[name]: value});
  // }
  //

  submit = values => {
    const {dispatch} = this.props;
    dispatch(authActions.login(values.email, values.password))
  };

  // handleSubmit(e) {
  // 	e.preventDefault();
  //
  // 	this.setState({submitted: true});
  // 	const {email, password} = this.state;
  // 	const {dispatch} = this.props;
  // 	if (email && password) {
  // 		dispatch(usersActions.login(email, password));
  // 	}
  // }

  render() {
    const {loggingIn, error, errorMessage, loggedIn, classes} = this.props;
    // const {email, password, submitted} = this.state;
    if (loggedIn) {
      return (
        <Redirect to={{pathname: '/', state: {from: this.props.location}}}/>
      );

    }
    else {
      return (
        <div>
          <Grid container className={classes.root} justify="center">
            <ItemGrid xs={12} sm={6} md={4} lg={3}>
              <RegularCard
                cardTitle="Please, log in."
                content={<Grid justify="center" container className={classes.formGridContainer}>
                  <ItemGrid xs={12}>
                    <LoginForm onSubmit={this.submit} loggingIn={loggingIn}/>
                  </ItemGrid>
                  {error ?
                    <ItemGrid xs={12}>
                      <SnackbarContent
                        message={errorMessage}
                        color="danger"
                      />
                    </ItemGrid> : null}
                </Grid>
                }
              />
            </ItemGrid>
          </Grid>
        </div>
      );

    }
  }
}

LoginPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
  const {loggingIn, error, errorMessage, loggedIn} = state.auth;
  return {
    loggingIn, error, errorMessage, loggedIn
  };
}

const connectedLoginPage = connect(mapStateToProps)(withStyles(styles)(LoginPage));
export {connectedLoginPage as LoginPage}