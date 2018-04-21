import React from "react";
import {Paper, withStyles} from "material-ui";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import CustomTable from "modules/front/components/ShoppingCart/CustomTable/CustomTable";

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
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
      </Paper>
    );
  }
}

export default connect()(withStyles(styles)(ShoppingCartPage));