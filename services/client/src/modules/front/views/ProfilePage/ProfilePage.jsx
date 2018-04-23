import React from "react";
import {Grid, Paper, withStyles} from "material-ui";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";
import _ from 'lodash';
import UserForm from "modules/front/forms/UserForm";
import {usersActions} from "actions/users.actions";
import UserOrdersTable from "./UserOrdersTable";
import {ordersActions} from "actions/orders.actions";

const styles = {
  paper: {
    padding: 50,
    marginBottom: 50
  }
};

class ProfilePage extends React.Component {
  submit = values => {
    const {dispatch, user} = this.props;

    if (values["phone"]) {
      values["phone"] = values["phone"].replace(/\s/g, "");
    }

    if (values["zip_code"]) {
      values["zip_code"] = values["zip_code"].replace(/\s/g, "");
    }

    const attrs = ['firstName', 'lastName', 'phone', 'street', 'zipCode', 'city', 'country'];
    _.forEach(attrs, attr => {
      if (!_.has(values, attr)) {
        values[attr] = null;
      }
    });

    const formattedValues = _.mapKeys(values, (value, key) => _.snakeCase(key));

    console.log(formattedValues);

    dispatch(usersActions.update(user["id"], formattedValues))
  };

  componentDidUpdate() {
    const {dispatch, user} = this.props;

    if (user) {
      dispatch(ordersActions.getAllByUser(user["id"]))
    }
  }

  render() {
    const {classes, loggedIn, checkedLoggedIn, user, orders} = this.props;

    const formattedUser = _.mapKeys(user, (value, key) => _.camelCase(key));

    return (
      checkedLoggedIn && (
        loggedIn ? (
          <Grid container>
            <Grid item xs={12} sm={6}>
              <Paper className={classes.paper}>
                <UserForm onSubmit={this.submit} data={formattedUser}/>
              </Paper>
              <Paper className={classes.paper}>
                <UserOrdersTable orders={orders}/>
              </Paper>
            </Grid>
          </Grid>
        ) : (
          <Redirect to="/login"/>
        )
      )
    );
  }
}

const mapStateToProps = state => ({
  loggedIn: state.auth.loggedIn,
  checkedLoggedIn: state.auth.checkedLoggedIn,
  user: state.auth.user,
  orders: state.orders.itemsByUser
});
export default connect(mapStateToProps)(withStyles(styles)(ProfilePage));