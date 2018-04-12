import {usersConstants} from 'constants/users.constants';
import {usersService} from 'services/users.service';
import {history} from 'helpers';

export const usersActions = {
	getAll,
	delete: _delete
};

// const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function getAll() {
	return dispatch => {
		dispatch(request());

		usersService.getAll()
			.then(
				users => dispatch(success(users)),
				error => dispatch(failure(error))
			);
	};

	function request() {
		return {type: usersConstants.GETALL_REQUEST}
	}

	function success(users) {
		return {type: usersConstants.GETALL_SUCCESS, users}
	}

	function failure(error) {
		return {type: usersConstants.GETALL_FAILURE, error}
	}
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
	return dispatch => {
		dispatch(request(id));

		usersService.delete(id)
			.then(
				user => {
					dispatch(success(id));
				},
				error => {
					dispatch(failure(id, error));
				}
			);
	};

	function request(id) {
		return {type: usersConstants.DELETE_REQUEST, id}
	}

	function success(id) {
		return {type: usersConstants.DELETE_SUCCESS, id}
	}

	function failure(id, error) {
		return {type: usersConstants.DELETE_FAILURE, id, error}
	}
}