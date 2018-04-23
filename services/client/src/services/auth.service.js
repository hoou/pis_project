// import fetch from 'cross-fetch'
import {authHeader} from 'helpers';
import {apiConstants} from "constants/api.constants"
import {handleResponse} from "./helpers/handleResponse";

export const authService = {
  login,
  logout,
  status
};

function status() {
  const requestOptions = {
    method: 'GET',
    headers: authHeader()
  };

  return fetch(apiConstants.URL + '/auth/status', requestOptions).then(handleResponse)
}


function login(email, password) {
  const requestOptions = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: email, password: password})
  };

  return fetch(apiConstants.URL + '/auth/login', requestOptions)
    .then(handleResponse)
    .then(data => {
        if (data && data['access_token'] && data['refresh_token']) {
          localStorage.setItem('access_token', JSON.stringify(data['access_token']));
          localStorage.setItem('refresh_token', JSON.stringify(data['refresh_token']));
          return data;
        } else {
          return Promise.reject("Login failed. Please, try again.")
        }
      }
    )
}

function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}
