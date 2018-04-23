import {authConstants} from 'constants/auth.constants';
import {authService} from 'services/auth.service';
import {history} from 'helpers';
import {alertActions} from "actions/alert.actions";

const authActions = {
  checkAdmin,
  status,
  login,
  logout
};

export default authActions;

function checkAdmin() {
  return dispatch => {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken)
      dispatch(failure());
    else
      authService.status()
        .then(
          data => {
            const role = data["role_name"];
            if (role === "admin" || role === "worker") {
              dispatch(success())
            } else {
              history.push('/admin/login');
              dispatch(alertActions.error("This is only for admin and workers!"));
              dispatch(failure());
            }
          },
          error => {
            history.push('/admin/login');
            dispatch(alertActions.error(error));
            dispatch(failure())
          }
        )
  };

  function success() {
    return {type: authConstants.CHECK_ADMIN_SUCCESS}
  }

  function failure() {
    return {type: authConstants.CHECK_ADMIN_FAILURE}
  }
}

function status() {
  return dispatch => {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken)
      dispatch(failure());
    else
      authService.status()
        .then(
          data => {
            dispatch(success(data));
          },
          error => {
            dispatch(alertActions.error(error));
            dispatch(failure());
          }
        )
  };

  function success(data) {
    return {type: authConstants.STATUS_SUCCESS, data}
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
          dispatch(checkAdmin());
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
