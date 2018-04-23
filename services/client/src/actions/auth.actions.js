import {authConstants} from 'constants/auth.constants';
import {authService} from 'services/auth.service';
import {history} from 'helpers';
import {alertActions} from "actions/alert.actions";

const authActions = {
  checkLoggedIn,
  status,
  login,
  logout
};

export default authActions;

function checkLoggedIn(asAdmin = true) {
  return dispatch => {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken)
      dispatch(failure());
    else
      authService.status()
        .then(
          data => {
            dispatch(authActions.status());
            if (asAdmin) {
              const role = data["role_name"];
              if (role === "admin" || role === "worker") {
                dispatch(success())
              } else {
                history.push('/admin/login');
                dispatch(alertActions.error("This is only for admin and workers!"));
                dispatch(failure());
              }
            } else {
              dispatch(success())
            }
          },
          error => {
            if (asAdmin) {
              history.push('/admin/login');
            } else {
              history.push('/login');
            }
            dispatch(alertActions.error(error));
            dispatch(failure())
          }
        )
  };

  function success() {
    return {type: authConstants.CHECK_LOGGED_IN_SUCCESS}
  }

  function failure() {
    return {type: authConstants.CHECK_LOGGED_IN_FAILURE}
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

function login(email, password, asAdmin = true) {
  return dispatch => {
    authService.login(email, password)
      .then(
        tokens => {
          dispatch(alertActions.clear());
          dispatch(success(tokens));

          if (asAdmin) {
            history.push('/admin');
            dispatch(checkLoggedIn());
          } else {
            dispatch(alertActions.success("You are logged in"));
            history.push('/home');
          }
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
