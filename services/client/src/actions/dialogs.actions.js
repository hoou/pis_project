import {dialogsConstants} from 'constants/dialogs.constants';

export const dialogsActions = {
  open,
  close
};

function open() {
  return {type: dialogsConstants.OPEN};
}

function close() {
  return {type: dialogsConstants.CLOSE};
}
