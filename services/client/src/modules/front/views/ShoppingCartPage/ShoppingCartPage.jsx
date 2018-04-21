import React from "react";
import {Button, Paper, withStyles} from "material-ui";
import CustomTable from "modules/front/components/ShoppingCart/CustomTable/CustomTable";
import {Link} from "react-router-dom";

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  checkoutButton: {
    float: "right",
    margin: 20
  }
});

const ShoppingCartPage = (props) => {
  const {classes, items} = props;
  return (
    <Paper className={classes.root}>
      <CustomTable items={items}/>
      <Link to="/checkout">
        <Button color="primary" className={classes.checkoutButton} variant="raised">
          Checkout
        </Button>
      </Link>
    </Paper>
  );
};

export default (withStyles(styles)(ShoppingCartPage));