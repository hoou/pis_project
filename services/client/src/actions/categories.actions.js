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
        },
        error => {
          dispatch(failure(error));
          dispatch(alertActions.error(error));
        }
      )
      .finally(() => dispatch(dialogsActions.close()));
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
    categoriesService.remove(id)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(categoriesActions.getAll())
        },
        error => dispatch(alertActions.error(error))
      );
  };
}

function update(id, values) {
  return dispatch => {
    categoriesService.update(id, values)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(categoriesActions.getAll())
        },
        error => dispatch(alertActions.error(error))
      )
      .finally(() => dispatch(dialogsActions.close()))
  }
}