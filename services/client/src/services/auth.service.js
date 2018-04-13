// import fetch from 'cross-fetch'
import {authHeader} from 'helpers';
import {apiConstants} from "constants/api.constants"

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

  return fetch(apiConstants.URL + '/auth/status', requestOptions)
    .then(response => {
      if (!response.ok) {
        return Promise.reject(response.statusText);
      }

      return response.json();
    })
    .then(data => {
        return data.role;
      }
    )
}


function login(email, password) {
  const requestOptions = {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: email, password: password})
  };

  return fetch(apiConstants.URL + '/auth/login', requestOptions)
    .then(response => {
      if (!response.ok) {
        return Promise.reject('Incorrect email or password');
      }

      return response.json();
    })
    .then(data => {
        // login successful if there's a jwt token in the response
        if (data && data['access_token'] && data['refresh_token']) {
          // store user details and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('access_token', JSON.stringify(data['access_token']));
          localStorage.setItem('refresh_token', JSON.stringify(data['refresh_token']));
        }

        return data;
      }
    )
}

function logout() {
  // remove user from local storage to log user out
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}
