import {ordersConstants} from 'constants/orders.constants';

const initialState = {
  items: [],
  itemsByUser: []
};

export function ordersReducer(state = initialState, action) {
  switch (action.type) {
    case ordersConstants.GETALL_SUCCESS:
      return {
        ...state,
        items: action.orders
      };
    case ordersConstants.GETALLBYUSER_SUCCESS:
      return {
        ...state,
        itemsByUser: action.orders
      };
    default:
      return state
  }
}