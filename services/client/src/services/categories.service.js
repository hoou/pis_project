// import fetch from 'cross-fetch'
import {authHeader} from 'helpers';
import {apiConstants} from 'constants/api.constants'
import {handleResponse} from "./helpers/handleResponse";

export const categoriesService = {
  add,
  getAll,
  // getById,
  // update,
  remove
};

function add(name) {
  const requestOptions = {
    method: 'POST',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify({name: name})
  };

  return fetch(apiConstants.URL + '/categories/', requestOptions).then(handleResponse);
}

function getAll() {
  const requestOptions = {
    method: 'GET',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/categories/', requestOptions).then(handleResponse);
}

// function getById(id) {
//   const requestOptions = {
//     method: 'GET',
//     headers: authHeader()
//   };
//
//   return fetch('/users/' + id, requestOptions).then(handleResponse);
// }

// function update(user) {
//   const requestOptions = {
//     method: 'PUT',
//     headers: {...authHeader(), 'Content-Type': 'application/json'},
//     body: JSON.stringify(user)
//   };
//
//   return fetch('/users/' + user.id, requestOptions).then(handleResponse);
// }

function remove(id) {
  const requestOptions = {
    method: 'DELETE',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/categories/' + id, requestOptions).then(handleResponse);
}
