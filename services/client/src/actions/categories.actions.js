import {categoriesConstants} from 'constants/categories.constants';
import {categoriesService} from 'services/categories.service';
import {alertActions} from "actions/alert.actions"
import {dialogsActions} from "./dialogs.actions";

export const categoriesActions = {
  getAll,
  add,
  remove,
  update
};

function getAll() {
  return dispatch => {
    categoriesService.getAll()
      .then(
        categories => dispatch(success(categories)),
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
        }
      );
  };

  function success(categories) {
    return {type: categoriesConstants.GETALL_SUCCESS, categories}
  }

  function failure() {
    return {type: categoriesConstants.GETALL_FAILURE}
  }
}

function add(name) {
  return dispatch => {
    categoriesService.add(name)
      .then(
        data => {
          dispatch(alertActions.success(data.message));
          dispatch(categoriesActions.getAll());
          dispatch(success());
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      )
      .finally(() => dispatch(dialogsActions.close()));
  };

  function success() {
    return {type: categoriesConstants.ADD_SUCCESS}
  }

  function failure() {
    return {type: categoriesConstants.ADD_FAILURE}
  }
}

function remove(id) {
  return dispatch => {
    categoriesService.remove(id)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(categoriesActions.getAll());
          dispatch(success());
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      );
  };

  function success() {
    return {type: categoriesConstants.REMOVE_SUCCESS}
  }

  function failure() {
    return {type: categoriesConstants.REMOVE_FAILURE}
  }
}

function update(id, values) {
  return dispatch => {
    categoriesService.update(id, values)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(categoriesActions.getAll());
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
    return {type: categoriesConstants.UPDATE_SUCCESS}
  }

  function failure() {
    return {type: categoriesConstants.UPDATE_FAILURE}
  }
}