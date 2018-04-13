import {categoriesConstants} from 'constants/categories.constants';

const initialState = {
  sentRequest: false,
  items: [],
};

export function categoriesReducer(state = initialState, action) {
  switch (action.type) {
    case categoriesConstants.GETALL_REQUEST:
      return {
        ...state,
        sentRequest: true
      };
    case categoriesConstants.GETALL_SUCCESS:
      return {
        ...state,
        sentRequest: false,
        items: action.categories
      };
    case categoriesConstants.GETALL_FAILURE:
      return {
        ...state,
        sentRequest: false,
      };
    case categoriesConstants.ADD_REQUEST:
      return {
        ...state,
        sentRequest: true
      };
    case categoriesConstants.ADD_SUCCESS:
      return {
        ...state,
        sentRequest: false,
      };
    case categoriesConstants.ADD_FAILURE:
      return {
        ...state,
        sentRequest: false,
      };
    default:
      return state
  }
}