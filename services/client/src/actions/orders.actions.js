import {ordersConstants} from "constants/orders.constants";
import {checkoutActions} from "actions/checkout.actions";
import {ordersService} from "services/orders.service";
import {shoppingCartActions} from "actions/shoppingCart.actions";
import {history} from "helpers";
import {alertActions} from "actions/alert.actions";
import {dialogsActions} from "./dialogs.actions";

export const ordersActions = {
  add,
  getAll,
  updateStatus
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

function updateStatus(id, status) {
  return dispatch => {
    ordersService.updateStatus(id, status)
      .then(
        data => {
          dispatch(alertActions.success(data.message));
          dispatch(ordersActions.getAll());
          dispatch(success())
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
        }
      )
      .finally(() => dispatch(dialogsActions.close()))
  };

  function success() {
    return {type: ordersConstants.UPDATE_STATUS_SUCCESS}
  }

  function failure() {
    return {type: ordersConstants.UPDATE_STATUS_FAILURE}
  }
}

function getAll() {
  return dispatch => {
    ordersService.getAll()
      .then(
        orders => {
          dispatch(success(orders))
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
        }
      );
  };

  function success(orders) {
    return {type: ordersConstants.GETALL_SUCCESS, orders: orders}
  }

  function failure() {
    return {type: ordersConstants.GETALL_FAILURE}
  }
}
