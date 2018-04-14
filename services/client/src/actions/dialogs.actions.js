import {dialogsConstants} from 'constants/dialogs.constants';

export const dialogsActions = {
  showNew,
  showEdit,
  close,
};

function showNew(title) {
  return {type: dialogsConstants.SHOW_NEW, title};
}

function showEdit(title, id) {
  return {type: dialogsConstants.SHOW_EDIT, title, id};
}

function close() {
  return {type: dialogsConstants.CLOSE};
}
