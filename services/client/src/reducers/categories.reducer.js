import {categoriesConstants} from 'constants/categories.constants';

const initialState = {
  items: [],
};

export function categoriesReducer(state = initialState, action) {
  switch (action.type) {
    case categoriesConstants.GETALL_SUCCESS:
      return {
        ...state,
        items: action.categories
      };
    default:
      return state
  }
}