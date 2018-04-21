import {checkoutConstants} from 'constants/checkout.constants';

const stepsCount = 3;

const initialState = {
  activeStep: 0,
  address: null,
  shippingAndPayment: null
};

export function checkoutReducer(state = initialState, action) {
  switch (action.type) {
    case checkoutConstants.NEXT:
      return {
        ...state,
        activeStep: state.activeStep < stepsCount ? state.activeStep + 1 : stepsCount
      };
    case checkoutConstants.BACK:
      return {
        ...state,
        activeStep: state.activeStep > 0 ? state.activeStep - 1 : 0
      };
    case checkoutConstants.RESET:
      return {
        ...initialState
      };
    case checkoutConstants.SUBMIT_ADDRESS:
      return {
        ...state,
        address: action.values
      };
    case checkoutConstants.SUBMIT_SHIPPING_AND_PAYMENT:
      console.log("shipping and payment v reduceri", action.values);
      return {
        ...state,
        shippingAndPayment: action.values
      };
    default:
      return state
  }
}