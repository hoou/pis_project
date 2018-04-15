import {dialogsConstants} from 'constants/dialogs.constants';

const initialState = {
  open: false,
  title: '',
  edit: false,
  editId: null
};

export function dialogsReducer(state = initialState, action) {
  switch (action.type) {
    case dialogsConstants.SHOW_NEW:
      return {
        open: true,
        title: action.title,
        edit: false
      };
    case dialogsConstants.SHOW_EDIT:
      return {
        open: true,
        title: action.title,
        edit: true,
        editId: action.id
      };
    case dialogsConstants.CLOSE:
      return {
        ...state,
        open: false
      };
    default:
      return state
  }
}