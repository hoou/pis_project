import {ordersConstants} from "constants/orders.constants";
import {checkoutActions} from "actions/checkout.actions";
import {ordersService} from "services/orders.service";
import {shoppingCartActions} from "actions/shoppingCart.actions";
import {history} from "helpers";
import {alertActions} from "actions/alert.actions";

export const ordersActions = {
  add
};

function add(items, address) {
  return dispatch => {
    ordersService.add(items, address)
      .then(
        data => {
          dispatch(alertActions.success(data.message));
          dispatch(shoppingCartActions.reset());
          dispatch(checkoutActions.reset());
          dispatch(success())
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
        }
      )
      .finally(
        () => {
          history.push('/home');
        }
      )
  };

  function success() {
    return {type: ordersConstants.ADD_SUCCESS}
  }

  function failure() {
    return {type: ordersConstants.ADD_FAILURE}
  }
}
