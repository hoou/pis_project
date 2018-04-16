import {dialogsConstants} from 'constants/dialogs.constants';

export const dialogsActions = {
  showNew,
  showEdit,
  close,
};

function showNew(form) {
  return {type: dialogsConstants.SHOW_NEW, form: form};
}

function showEdit(form, id) {
  return {type: dialogsConstants.SHOW_EDIT, form: form, id};
}

function close() {
  return {type: dialogsConstants.CLOSE};
}
