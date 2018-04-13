import {authConstants} from 'constants/auth.constants';

let access_token = JSON.parse(localStorage.getItem('access_token'));

const initialState = {
  checkedStatus: false,
  loggedIn: false,
  role: null,
  loggingIn: false,
  tokens: null
};

export function authReducer(state = initialState, action) {
  switch (action.type) {
    case authConstants.STATUS_SUCCESS:
      return {
        ...state,
        checkedStatus: true,
        loggedIn: true,
        role: action.role
      };
    case authConstants.STATUS_FAILURE:
      return {
        ...state,
        checkedStatus: true,
        loggedIn: false,
        tokens: null
      };
    case authConstants.LOGIN_REQUEST:
      return {
        ...state,
        loggingIn: true
      };
    case authConstants.LOGIN_SUCCESS:
      return {
        ...state,
        loggedIn: true,
        error: false,
        tokens: action.tokens,
        loggingIn: false
      };
    case authConstants.LOGIN_FAILURE:
      return {
        ...state,
        loggingIn: false,
        error: true,
        errorMessage: action.error
      };
    case authConstants.LOGOUT:
      return {
        ...state,
        loggedIn: false,
        tokens: null
      };
    default:
      return state
  }
}