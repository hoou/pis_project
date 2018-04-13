import {dialogsConstants} from 'constants/dialogs.constants';

const initialState = {open: false};

export function dialogsReducer(state = initialState, action) {
  switch (action.type) {
    case dialogsConstants.OPEN:
      return {
        open: true
      };
    case dialogsConstants.CLOSE:
      return {
        open: false
      };
    default:
      return state
  }
}