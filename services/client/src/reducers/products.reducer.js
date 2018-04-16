import {productsConstants} from 'constants/products.constants';

const initialState = {
  items: [],
};

export function productsReducer(state = initialState, action) {
  switch (action.type) {
    case productsConstants.GETALL_SUCCESS:
      return {
        ...state,
        items: action.products
      };
    default:
      return state
  }
}