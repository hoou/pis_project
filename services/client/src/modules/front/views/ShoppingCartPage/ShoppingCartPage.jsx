import React from "react";
import {Button, Paper, withStyles} from "material-ui";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
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

class ShoppingCartPage extends React.Component {
  constructor(props) {
    super(props);
    const {dispatch} = props;

    dispatch(productsActions.getAll());
  }

  render() {
    const {classes} = this.props;

    return (
      <Paper className={classes.root}>
        <CustomTable/>
        <Link to="/checkout">
          <Button color="primary" className={classes.checkoutButton} variant="raised">
            Checkout
          </Button>
        </Link>
      </Paper>
    );
  }
}

export default connect()(withStyles(styles)(ShoppingCartPage));