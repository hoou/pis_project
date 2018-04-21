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
      localStorage.setItem('shoppingCartItems', JSON.stringify(newItems));
      return {
        ...state,
        items: newItems
      };
    case shoppingCartConstants.REMOVE:
      let index = _.findIndex(state.items, item => item === action.id);
      if (index !== -1) {
        let newItems = state.items.slice();
        newItems.splice(index, 1);
        localStorage.setItem('shoppingCartItems', JSON.stringify(newItems));
        return {
          ...state,
          items: newItems
        };
      } else {
        return state;
      }
    case shoppingCartConstants.LOAD_FROM_LOCAL_STORAGE:
      return {
        ...state,
        items: action.items
      };
    default:
      return state
  }
}