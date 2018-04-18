import {productsConstants} from 'constants/products.constants';
import {productsService} from 'services/products.service';
import {alertActions} from "actions/alert.actions"
import {dialogsActions} from "./dialogs.actions";

export const productsActions = {
  getAll,
  getAllDeleted,
  add,
  remove,
  update,
  restore
};

function getAll() {
  return dispatch => {
    productsService.getAll()
      .then(
        products => dispatch(success(products)),
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
        }
      );
  };

  function success(products) {
    return {type: productsConstants.GETALL_SUCCESS, products: products}
  }

  function failure() {
    return {type: productsConstants.GETALL_FAILURE}
  }
}

function getAllDeleted() {
  return dispatch => {
    productsService.getAllDeleted()
      .then(
        products => dispatch(success(products)),
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
        }
      );
  };

  function success(products) {
    return {type: productsConstants.GETALL_DELETED_SUCCESS, products: products}
  }

  function failure() {
    return {type: productsConstants.GETALL_DELETED_FAILURE}
  }
}

function add(category_id, values) {
  return dispatch => {
    productsService.add(category_id, values)
      .then(
        data => {
          dispatch(alertActions.success(data.message));
          dispatch(productsActions.getAll());
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
    return {type: productsConstants.ADD_SUCCESS}
  }

  function failure() {
    return {type: productsConstants.ADD_FAILURE}
  }
}

function remove(id) {
  return dispatch => {
    productsService.remove(id)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(productsActions.getAll());
          dispatch(productsActions.getAllDeleted());
          dispatch(success());
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      );
  };

  function success() {
    return {type: productsConstants.REMOVE_SUCCESS}
  }

  function failure() {
    return {type: productsConstants.REMOVE_FAILURE}
  }
}

function restore(id) {
  return dispatch => {
    productsService.restore(id)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(productsActions.getAll());
          dispatch(productsActions.getAllDeleted());
          dispatch(success());
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      );
  };

  function success() {
    return {type: productsConstants.RESTORE_SUCCESS}
  }

  function failure() {
    return {type: productsConstants.RESTORE_FAILURE}
  }
}

function update(id, values) {
  return dispatch => {
    productsService.update(id, values)
      .then(
        data => {
          dispatch(alertActions.success(data["message"]));
          dispatch(productsActions.getAll());
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
    return {type: productsConstants.UPDATE_SUCCESS}
  }

  function failure() {
    return {type: productsConstants.UPDATE_FAILURE}
  }
}