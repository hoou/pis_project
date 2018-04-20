// import fetch from 'cross-fetch'
import {authHeader} from 'helpers';
import {apiConstants} from 'constants/api.constants'
import {handleResponse} from "./helpers/handleResponse";

export const productsService = {
  add,
  addImages,
  get,
  getAll,
  getAllDeleted,
  update,
  remove,
  restore
};

function add(category_id, values) {
  const requestOptions = {
    method: 'POST',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify(values)
  };

  return fetch(apiConstants.URL + '/categories/' + category_id + '/products', requestOptions).then(handleResponse);
}

function addImages(product_id, files) {
  let formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("file" + i, files[i]);
  }

  const requestOptions = {
    method: 'POST',
    headers: {...authHeader()},
    body: formData
  };

  return fetch(apiConstants.URL + '/products/' + product_id + '/images', requestOptions).then(handleResponse);
}

function get(id) {
  const requestOptions = {
    method: 'GET'
  };

  return fetch(apiConstants.URL + '/products/' + id, requestOptions).then(handleResponse);
}

function getAll() {
  const requestOptions = {
    method: 'GET'
  };

  return fetch(apiConstants.URL + '/products/', requestOptions).then(handleResponse);
}

function getAllDeleted() {
  const requestOptions = {
    method: 'GET',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/products/deleted', requestOptions).then(handleResponse);
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

function restore(id) {
  const requestOptions = {
    method: 'PATCH',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/products/' + id + '/restore', requestOptions).then(handleResponse);
}
