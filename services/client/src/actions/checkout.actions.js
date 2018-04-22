import {checkoutConstants} from 'constants/checkout.constants';
import {ordersService} from "../services/orders.service";
import {alertActions} from "./alert.actions";
import {shoppingCartActions} from "./shoppingCart.actions";
import {history} from "../helpers";

export const checkoutActions = {
  next,
  back,
  reset,
  submitAddress,
  submitShippingAndPayment,
  loadFromLocalStorage,
  createOrder,
};

function next() {
  return {type: checkoutConstants.NEXT};
}

function back() {
  return {type: checkoutConstants.BACK};
}

function reset() {
  localStorage.removeItem('checkoutAddress');
  localStorage.removeItem('checkoutShippingAndPayment');
  return {type: checkoutConstants.RESET};
}

function submitAddress(values) {
  localStorage.setItem('checkoutAddress', JSON.stringify(values));
  return {type: checkoutConstants.SUBMIT_ADDRESS, values};
}

function submitShippingAndPayment(values) {
  localStorage.setItem('checkoutShippingAndPayment', JSON.stringify(values));
  return {type: checkoutConstants.SUBMIT_SHIPPING_AND_PAYMENT, values};
}

function loadFromLocalStorage() {
  let shippingAndPayment = localStorage.getItem("checkoutShippingAndPayment");
  let address = localStorage.getItem("checkoutAddress");
  if (shippingAndPayment) {
    shippingAndPayment = JSON.parse(shippingAndPayment)
  } else {
    shippingAndPayment = null;
  }

  if (address) {
    address = JSON.parse(address)
  } else {
    address = null;
  }
  return {type: checkoutConstants.LOAD_FROM_LOCAL_STORAGE, shippingAndPayment, address};
}

function createOrder(items, address) {
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
    return {type: checkoutConstants.CREATE_ORDER_SUCCESS}
  }

  function failure() {
    return {type: checkoutConstants.CREATE_ORDER_FAILURE}
  }
}
