import {authConstants} from 'constants/auth.constants';

const initialState = {
  checkedAdmin: false,
  loggedIn: false,
  user: null,
  tokens: null
};

export function authReducer(state = initialState, action) {
  switch (action.type) {
    case authConstants.CHECK_ADMIN_SUCCESS:
      return {
        ...state,
        loggedIn: true,
        checkedAdmin: true
      };
    case authConstants.CHECK_ADMIN_FAILURE:
      return {
        ...state,
        loggedIn: false,
        tokens: null,
        checkedAdmin: true
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