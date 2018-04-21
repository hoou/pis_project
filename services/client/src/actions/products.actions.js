import _ from "lodash"
import {productsConstants} from 'constants/products.constants';
import {productsService} from 'services/products.service';
import {alertActions} from "actions/alert.actions"
import {dialogsActions} from "./dialogs.actions";

export const productsActions = {
  get,
  getAll,
  getAllDeleted,
  add,
  remove,
  update,
  restore,
  addImage
};

function get(id) {
  return dispatch => {
    productsService.get(id)
      .then(
        product => dispatch(success(product)),
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure());
        }
      );
  };

  function success(product) {
    return {type: productsConstants.GET_SUCCESS, product: product}
  }

  function failure() {
    return {type: productsConstants.GET_FAILURE}
  }
}

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
    productsService.add(category_id, _.omit(values, "images"))
      .then(
        data => {
          if (values["images"]) {
            const new_product_id = data.data.id;
            productsService.addImages(new_product_id, values["images"])
              .then(
                () => {
                  dispatch(productsActions.getAll());
                  dispatch(alertActions.data.message);
                  dispatch(success());
                },
                error => {
                  dispatch(alertActions.error(error));
                  dispatch(failure())
                }
              );
          } else {
            dispatch(productsActions.getAll());
            dispatch(alertActions.data.message);
            dispatch(success());
          }
        },
        error => {
          dispatch(alertActions.error(error));
          dispatch(failure())
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

function addImage(product_id, file) {
  return dispatch => {
    productsService.addImages(product_id, file)
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
    return {type: productsConstants.ADD_IMAGE_SUCCESS}
  }

  function failure() {
    return {type: productsConstants.ADD_IMAGE_FAILURE}
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