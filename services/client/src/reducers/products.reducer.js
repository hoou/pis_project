import {productsConstants} from 'constants/products.constants';

const initialState = {
  items: [],
  deleted_items: [],
  detail: null,
  ratingsByProduct: [],
  gotItems: false,
};

export function productsReducer(state = initialState, action) {
  switch (action.type) {
    case productsConstants.GET_SUCCESS:
      return {
        ...state,
        detail: action.product
      };
    case productsConstants.GETALL_SUCCESS:
      return {
        ...state,
        items: action.products
      };
    case productsConstants.GET_RATINGS_SUCCESS:
      return {
        ...state,
        ratingsByProduct: action.data,
      };
    case productsConstants.GETALL_DELETED_SUCCESS:
      return {
        ...state,
        deleted_items: action.products
      };
    default:
      return state
  }
}