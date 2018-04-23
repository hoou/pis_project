import {authHeader} from 'helpers';
import {apiConstants} from 'constants/api.constants'
import {handleResponse} from "./helpers/handleResponse";

export const usersService = {
  getById,
  update,
};

function getById(id) {
  const requestOptions = {
    method: 'GET',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/users/' + id, requestOptions).then(handleResponse);
}

function update(id, values) {
  const requestOptions = {
    method: 'PATCH',
    headers: {...authHeader(), 'Content-Type': 'application/json'},
    body: JSON.stringify(values)
  };

  return fetch(apiConstants.URL + '/users/' + id, requestOptions).then(handleResponse);
}