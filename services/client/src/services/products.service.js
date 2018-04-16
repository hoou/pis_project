// import fetch from 'cross-fetch'
import {authHeader} from 'helpers';
import {apiConstants} from 'constants/api.constants'
import {handleResponse} from "./helpers/handleResponse";

export const productsService = {
  add,
  getAll,
  update,
  remove
};

function add(category_id, values) {
  const requestOptions = {
    method: 'POST',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify(values)
  };

  return fetch(apiConstants.URL + '/categories/' + category_id + '/products', requestOptions).then(handleResponse);
}

function getAll() {
  const requestOptions = {
    method: 'GET',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/products/', requestOptions).then(handleResponse);
}

function update(id, values) {
  console.log(values);
  const requestOptions = {
    method: 'PATCH',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify(values)
  };

  return fetch(apiConstants.URL + '/products/' + id, requestOptions).then(handleResponse);
}

function remove(id) {
  const requestOptions = {
    method: 'DELETE',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/products/' + id, requestOptions).then(handleResponse);
}
