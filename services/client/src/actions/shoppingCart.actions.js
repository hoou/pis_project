import _ from "lodash"
import {shoppingCartConstants} from 'constants/shoppingCart.constants';

export const shoppingCartActions = {
  add,
  remove,
  loadFromLocalStorage,
  checkItems,
  reset
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

function checkItems(products) {
  let items = JSON.parse(localStorage.getItem("shoppingCartItems"));
  items = _.filter(items, item => (_.find(products, o => (o.id === item)) !== undefined));
  return {type: shoppingCartConstants.CHECK_ITEMS, items}
}

function reset() {
  localStorage.removeItem("shoppingCartItems");
  return {type: shoppingCartConstants.RESET}
}
