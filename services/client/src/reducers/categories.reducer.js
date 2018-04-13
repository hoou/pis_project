import {categoriesConstants} from 'constants/categories.constants';

export function categoriesReducer(state = {}, action) {
  switch (action.type) {
    case categoriesConstants.GETALL_REQUEST:
      return {
        loading: true
      };
    case categoriesConstants.GETALL_SUCCESS:
      return {
        items: action.categories
      };
    case categoriesConstants.GETALL_FAILURE:
      return {
        error: action.error
      };
    // case usersConstants.DELETE_REQUEST:
    //   // add 'deleting:true' property to user being deleted
    //   return {
    //     ...state,
    //     items: state.items.map(user =>
    //       user.id === action.id
    //         ? {...user, deleting: true}
    //         : user
    //     )
    //   };
    // case usersConstants.DELETE_SUCCESS:
    //   // remove deleted user from state
    //   return {
    //     items: state.items.filter(user => user.id !== action.id)
    //   };
    // case usersConstants.DELETE_FAILURE:
    //   // remove 'deleting:true' property and add 'deleteError:[error]' property to user
    //   return {
    //     ...state,
    //     items: state.items.map(user => {
    //       if (user.id === action.id) {
    //         // make copy of user without 'deleting:true' property
    //         const {deleting, ...userCopy} = user;
    //         // return copy of user with 'deleteError:[error]' property
    //         return {...userCopy, deleteError: action.error};
    //       }
    //
    //       return user;
    //     })
    //   };
    default:
      return state
  }
}