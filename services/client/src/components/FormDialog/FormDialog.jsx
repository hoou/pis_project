import React from 'react';
import Button from 'components/CustomButtons/Button';
import {submit} from "redux-form"
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from 'material-ui/Dialog';
import {connect} from "react-redux";
import {dialogsActions} from "actions/dialogs.actions";

const FormDialog = props => {
  const {title, edit, contentText, form, dispatch, open} = props;

  const handleClose = () => dispatch(dialogsActions.close());
  const handleClickCancel = handleClose;
  const handleClickSend = () => dispatch(submit(form.type.Naked.name));

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">{edit ? "Edit " : "Add new "}{title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {contentText}
          </DialogContentText>
          {form}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClickCancel} color="primary">
            Cancel
          </Button>
          <Button onClick={handleClickSend} color="primary">
            Send
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

function mapStateToProps(state) {
  const {open, title, edit} = state.dialogs;
  return {
    open, title, edit
  }
}

export default connect(mapStateToProps)(FormDialog);