import {categoriesConstants} from 'constants/categories.constants';
import {categoriesService} from 'services/categories.service';

export const categoriesActions = {
  getAll,
  // delete: _delete
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

// prefixed function name with underscore because delete is a reserved word in javascript
// function _delete(id) {
//   return dispatch => {
//     dispatch(request(id));
//
//     usersService.delete(id)
//       .then(
//         user => {
//           dispatch(success(id));
//         },
//         error => {
//           dispatch(failure(id, error));
//         }
//       );
//   };
//
//   function request(id) {
//     return {type: usersConstants.DELETE_REQUEST, id}
//   }
//
//   function success(id) {
//     return {type: usersConstants.DELETE_SUCCESS, id}
//   }
//
//   function failure(id, error) {
//     return {type: usersConstants.DELETE_FAILURE, id, error}
//   }
// }