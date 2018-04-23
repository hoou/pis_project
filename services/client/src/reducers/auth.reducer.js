import {authConstants} from 'constants/auth.constants';

const initialState = {
  checkedLoggedIn: false,
  loggedIn: false,
  user: null,
  tokens: null
};

export function authReducer(state = initialState, action) {
  switch (action.type) {
    case authConstants.CHECK_LOGGED_IN_SUCCESS:
      return {
        ...state,
        user: action.data,
        loggedIn: true,
        checkedLoggedIn: true
      };
    case authConstants.CHECK_LOGGED_IN_FAILURE:
      return {
        ...state,
        loggedIn: false,
        tokens: null,
        checkedLoggedIn: true
      };
    case authConstants.STATUS_SUCCESS:
      return {
        ...state,
        user: action.data
      };
    case authConstants.LOGIN_SUCCESS:
      return {
        ...state,
        loggedIn: true,
        tokens: action.tokens,
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