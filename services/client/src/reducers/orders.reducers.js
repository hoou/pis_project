import {ordersConstants} from 'constants/orders.constants';

const initialState = {
  items: []
};

export function ordersReducer(state = initialState, action) {
  switch (action.type) {
    case ordersConstants.GETALL_SUCCESS:
      return {
        ...state,
        items: action.orders
      };
    default:
      return state
  }
}