import {checkoutConstants} from 'constants/checkout.constants';

const stepsCount = 3;

const initialState = {
  activeStep: 0,
  address: null,
  shippingAndPayment: null,
  finished: false
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
      return {
        ...state,
        shippingAndPayment: action.values
      };
    case checkoutConstants.LOAD_FROM_LOCAL_STORAGE:
      return {
        ...state,
        address: action.address,
        shippingAndPayment: action.shippingAndPayment
      };
    case checkoutConstants.INIT: {
      return {
        ...state,
        finished: false
      }
    }
    case checkoutConstants.FINISH: {
      return {
        ...state,
        finished: true
      }
    }
    default:
      return state
  }
}