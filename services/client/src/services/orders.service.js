import {apiConstants} from "../constants/api.constants";
import {handleResponse} from "./helpers/handleResponse";

export const ordersService = {
  add
};

function add(items, address) {
  const requestOptions = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({items: items, delivery_address: address})
  };

  return fetch(apiConstants.URL + '/orders/', requestOptions).then(handleResponse);
}
