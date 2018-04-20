import {shoppingCartConstants} from 'constants/shoppingCart.constants';

export const shoppingCartActions = {
  add,
  remove
};

function add(id) {
  return {type: shoppingCartConstants.ADD, id};
}

function remove(id) {
  return {type: shoppingCartConstants.REMOVE, id};
}
