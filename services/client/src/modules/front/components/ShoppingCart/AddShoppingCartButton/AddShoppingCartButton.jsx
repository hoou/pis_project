import React from "react"
import {Button, IconButton, withStyles} from "material-ui";
import {AddShoppingCart} from "@material-ui/icons";
import {shoppingCartActions} from "actions/shoppingCart.actions";
import {connect} from "react-redux";

const styles = {
  icon: {
    marginRight: 10
  }
};

class AddShoppingCartButton extends React.Component {
  handleClick = () => {
    const {dispatch, id} = this.props;
    dispatch(shoppingCartActions.add(id));
  };

  render() {
    const {classes, raised} = this.props;
    return (
      !raised ? (
        <IconButton onClick={this.handleClick} aria-label="Add to cart">
          <AddShoppingCart/>
        </IconButton>
      ) : (
        <Button onClick={this.handleClick} aria-label="Add to cart" variant="raised">
          <AddShoppingCart className={classes.icon}/>
          add to cart
        </Button>
      )
    );
  }
}

export default connect()(withStyles(styles)(AddShoppingCartButton));