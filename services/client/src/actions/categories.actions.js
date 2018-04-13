import {categoriesConstants} from 'constants/categories.constants';
import {categoriesService} from 'services/categories.service';
import {alertActions} from "actions/alert.actions"
import {dialogsActions} from "./dialogs.actions";

export const categoriesActions = {
  getAll,
  add,
  remove
};

function getAll() {
  return dispatch => {
    dispatch(request());

    categoriesService.getAll()
      .then(
        categories => dispatch(success(categories)),
        error => dispatch(failure(error))
      );
  };

  function request() {
    return {type: categoriesConstants.GETALL_REQUEST}
  }

  function success(categories) {
    return {type: categoriesConstants.GETALL_SUCCESS, categories}
  }

  function failure(error) {
    return {type: categoriesConstants.GETALL_FAILURE, error}
  }
}

function add(name) {
  return dispatch => {
    dispatch(request(name));

    categoriesService.add(name)
      .then(
        data => {
          dispatch(success());
          dispatch(alertActions.success(data.message));
          dispatch(categoriesActions.getAll());
          dispatch(dialogsActions.close())
        },
        error => {
          dispatch(failure(error));
          dispatch(alertActions.error(error));
          dispatch(dialogsActions.close());
        }
      );
  };

  function request() {
    return {type: categoriesConstants.ADD_REQUEST}
  }

  function success() {
    return {type: categoriesConstants.ADD_SUCCESS}
  }

  function failure(error) {
    return {type: categoriesConstants.ADD_FAILURE, error}
  }
}

function remove(id) {
  return dispatch => {
    // dispatch(request(id));

    categoriesService.remove(id)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(categoriesActions.getAll())
          // dispatch(success(data["message"]));
        },
        error => {
          dispatch(alertActions.error(error));
          // dispatch(failure(error));
        }
      );
  };

  // function request() {
  //   return {type: categoriesConstants.DELETE_REQUEST}
  // }
  //
  // function success(message) {
  //   return {type: categoriesConstants.DELETE_SUCCESS, message}
  // }
  //
  // function failure(error) {
  //   return {type: categoriesConstants.DELETE_FAILURE, error}
  // }
}