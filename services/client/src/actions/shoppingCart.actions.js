import {shoppingCartConstants} from 'constants/shoppingCart.constants';

export const shoppingCartActions = {
  add,
  remove,
  loadFromLocalStorage
};

function add(id) {
  return {type: shoppingCartConstants.ADD, id};
}

function remove(id) {
  return {type: shoppingCartConstants.REMOVE, id};
}

function loadFromLocalStorage() {
  let items = localStorage.getItem("shoppingCartItems");
  return {type: shoppingCartConstants.LOAD_FROM_LOCAL_STORAGE, items: items ? JSON.parse(items) : []};
}
