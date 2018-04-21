import React from "react"
import {IconButton} from "material-ui";
import {AddShoppingCart} from "@material-ui/icons";
import {shoppingCartActions} from "actions/shoppingCart.actions";
import {connect} from "react-redux";

class AddShoppingCartButton extends React.Component {
  handleClick = () => {
    const {dispatch, id} = this.props;
    dispatch(shoppingCartActions.add(id));
  };

  render() {
    return (
      <IconButton onClick={this.handleClick} aria-label="Add to cart">
        <AddShoppingCart/>
      </IconButton>
    );
  }
}

export default connect()(AddShoppingCartButton);