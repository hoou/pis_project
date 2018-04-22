import {authConstants} from 'constants/auth.constants';

const initialState = {
  checkedStatus: false,
  loggedIn: false,
  role: null,
  email: null,
  tokens: null
};

export function authReducer(state = initialState, action) {
  switch (action.type) {
    case authConstants.STATUS_SUCCESS:
      return {
        ...state,
        checkedStatus: true,
        loggedIn: true,
        role: action.role,
        email: action.email
      };
    case authConstants.STATUS_FAILURE:
      return {
        ...state,
        checkedStatus: true,
        loggedIn: false,
        tokens: null
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