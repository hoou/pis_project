import _ from "lodash"
import {shoppingCartConstants} from 'constants/shoppingCart.constants';

const initialState = {
  items: []
};

export function shoppingCartReducer(state = initialState, action) {
  switch (action.type) {
    case shoppingCartConstants.ADD:
      let newItems = state.items.slice();
      newItems.push(action.id);
      return {
        ...state,
        items: newItems
      };
    case shoppingCartConstants.REMOVE:
      let index = _.findIndex(state.items, action.id);
      if (index !== -1) {
        return {
          ...state,
          items: state.items.splice(index, 1)
        };
      } else {
        return state;
      }
    default:
      return state
  }
}