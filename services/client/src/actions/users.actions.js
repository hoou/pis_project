import {alertActions} from "./alert.actions";
import {dialogsActions} from "./dialogs.actions";
import {usersService} from "services/users.service";
import {usersConstants} from "constants/users.constants";
import authActions from "./auth.actions";

export const usersActions = {
  update,
};

function update(id, values) {
  return dispatch => {
    usersService.update(id, values)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(authActions.status());
          dispatch(success());
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      )
      .finally(() => dispatch(dialogsActions.close()))
  };

  function success() {
    return {type: usersConstants.UPDATE_SUCCESS}
  }

  function failure() {
    return {type: usersConstants.UPDATE_FAILURE}
  }
}