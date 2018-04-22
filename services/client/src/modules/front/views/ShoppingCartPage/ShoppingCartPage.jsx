import React from "react";
import {Button, Paper, Typography, withStyles} from "material-ui";
import CustomTable from "modules/front/components/ShoppingCart/CustomTable/CustomTable";
import {Link} from "react-router-dom";
import _ from "lodash";

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
    minHeight: 300
  },
  checkoutButton: {
    float: "right",
    margin: 20
  },
  display: {
    marginTop: 100
  }
});

const ShoppingCartPage = (props) => {
  const {classes, products, items} = props;
  return (
    <Paper className={classes.root}>
      {_.size(items) > 0 ? (
        <div>
          <CustomTable products={products} items={items}/>
          <Link to="/checkout">
            <Button color="primary" className={classes.checkoutButton} variant="raised">
              Checkout
            </Button>
          </Link>
        </div>
      ) : (
        <Typography className={classes.display} variant="display2" align="center">
          No items in cart
        </Typography>
      )}
    </Paper>
  );
};

export default (withStyles(styles)(ShoppingCartPage));