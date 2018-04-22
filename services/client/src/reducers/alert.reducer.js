import { alertConstants } from 'constants/alert.constants';

const initialState = {
  type: null,
  message: null,
  openDialog: false
};

export function alertReducer(state = initialState, action) {
  switch (action.type) {
    case alertConstants.SUCCESS:
      return {
        ...state,
        type: 'success',
        message: action.message,
        openDialog: true
      };
    case alertConstants.ERROR:
      return {
        ...state,
        type: 'danger',
        message: action.message,
        openDialog: true
      };
    case alertConstants.CLEAR:
      return initialState;
    default:
      return state
  }
}