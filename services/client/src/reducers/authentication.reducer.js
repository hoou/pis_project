import {userConstants} from 'constants/user.constants';

let access_token = JSON.parse(localStorage.getItem('access_token'));
const initialState = access_token ? {loggedIn: true, user: {'name': 'TEST'}} : {};

export function authentication(state = initialState, action) {
	switch (action.type) {
		case userConstants.LOGIN_REQUEST:
			return {
				loggingIn: true
			};
		case userConstants.LOGIN_SUCCESS:
			return {
				loggedIn: true,
				user: action.user
			};
		case userConstants.LOGIN_FAILURE:
			return {
				error: true,
				errorMessage: action.error
			};
		case userConstants.LOGOUT:
			return {};
		default:
			return state
	}
}