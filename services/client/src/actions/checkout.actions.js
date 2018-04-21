import {checkoutConstants} from 'constants/checkout.constants';

export const checkoutActions = {
  next,
  back,
  reset,
  submitAddress,
  submitShippingAndPayment,
};

function next() {
  return {type: checkoutConstants.NEXT};
}

function back() {
  return {type: checkoutConstants.BACK};
}

function reset() {
  return {type: checkoutConstants.RESET};
}

function submitAddress(values) {
  return {type: checkoutConstants.SUBMIT_ADDRESS, values};
}

function submitShippingAndPayment(values) {
  return {type: checkoutConstants.SUBMIT_SHIPPING_AND_PAYMENT, values};
}