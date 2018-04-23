import {apiConstants} from "../constants/api.constants";
import {handleResponse} from "./helpers/handleResponse";
import {authHeader} from "helpers";

export const ordersService = {
  add,
  getAll,
  getAllByUser,
  updateStatus
};

function add(items, address) {
  const requestOptions = {
    method: 'POST',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify({items: items, delivery_address: address})
  };

  return fetch(apiConstants.URL + '/orders/', requestOptions).then(handleResponse);
}

function updateStatus(id, status) {
  const requestOptions = {
    method: 'PATCH',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify({status: status})
  };

  return fetch(apiConstants.URL + '/orders/' + id, requestOptions).then(handleResponse);
}

function getAll() {
  const requestOptions = {
    method: 'GET',
    headers: {...authHeader()}
  };

  return fetch(apiConstants.URL + '/orders/', requestOptions).then(handleResponse);
}

function getAllByUser(id) {
  const requestOptions = {
    method: 'GET',
    headers: {...authHeader()}
  };

  return fetch(apiConstants.URL + '/users/' + id + '/orders', requestOptions).then(handleResponse);
}
