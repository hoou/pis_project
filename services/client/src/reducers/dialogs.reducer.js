import {dialogsConstants} from 'constants/dialogs.constants';

const initialState = {
  open: false,
  form: null,
  edit: false,
  editId: null
};

export function dialogsReducer(state = initialState, action) {
  switch (action.type) {
    case dialogsConstants.SHOW_NEW:
      return {
        open: true,
        form: action.form,
        edit: false
      };
    case dialogsConstants.SHOW_EDIT:
      return {
        open: true,
        form: action.form,
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