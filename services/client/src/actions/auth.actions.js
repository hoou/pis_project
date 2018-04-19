import {authConstants} from 'constants/auth.constants';
import {authService} from 'services/auth.service';
import {history} from 'helpers';
import {alertActions} from "actions/alert.actions";

const authActions = {
  status,
  login,
  logout
};

export default authActions;

function status() {
  return dispatch => {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken)
      dispatch(failure());
    else
      authService.status()
        .then(data => {
          const role = data["role"];
          if (role === "admin" || role === "worker") {
            dispatch(success(role))
          } else {
            dispatch(failure());
          }
        })
        .catch(() => {
          dispatch(failure());
        });
  };

  function success(role) {
    return {type: authConstants.STATUS_SUCCESS, role}
  }

  function failure() {
    return {type: authConstants.STATUS_FAILURE}
  }
}

function login(email, password) {
  return dispatch => {
    authService.login(email, password)
      .then(
        tokens => {
          dispatch(alertActions.clear());
          history.push('/admin');
          dispatch(success(tokens));
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      );
  };

  function success(tokens) {
    return {type: authConstants.LOGIN_SUCCESS, tokens: tokens}
  }

  function failure() {
    return {type: authConstants.LOGIN_FAILURE}
  }
}

function logout() {
  authService.logout();
  return {type: authConstants.LOGOUT};
}
