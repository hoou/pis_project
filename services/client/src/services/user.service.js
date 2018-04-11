// import fetch from 'cross-fetch'
import {authHeader} from 'helpers';
import {apiConstants} from 'constants/api.constants'

export const userService = {
	login,
	logout,
	register,
	getAll,
	getById,
	update,
	delete: _delete
};

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
	localStorage.removeItem('user');
}

function getAll() {
	const requestOptions = {
		method: 'GET',
		headers: authHeader()
	};

	return fetch('/users', requestOptions).then(handleResponse);
}

function getById(id) {
	const requestOptions = {
		method: 'GET',
		headers: authHeader()
	};

	return fetch('/users/' + id, requestOptions).then(handleResponse);
}

function register(user) {
	const requestOptions = {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(user)
	};

	return fetch('/users/register', requestOptions).then(handleResponse);
}

function update(user) {
	const requestOptions = {
		method: 'PUT',
		headers: {...authHeader(), 'Content-Type': 'application/json'},
		body: JSON.stringify(user)
	};

	return fetch('/users/' + user.id, requestOptions).then(handleResponse);
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
	const requestOptions = {
		method: 'DELETE',
		headers: authHeader()
	};

	return fetch('/users/' + id, requestOptions).then(handleResponse);
}

function handleResponse(response) {
	if (!response.ok) {
		return Promise.reject(response.statusText);
	}

	return response.json();
}