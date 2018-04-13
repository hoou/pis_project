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
  const {title, contentText, form, dispatch, open} = props;

  const handleOpen = () => dispatch(dialogsActions.open());
  const handleClose = () => dispatch(dialogsActions.close());
  const handleSubmit = () => dispatch(submit(form.type.Naked.name));

  return (
    <div>
      <Button color="primary" onClick={handleOpen}>{title}</Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">{title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {contentText}
          </DialogContentText>
          {form}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Send
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

function mapStateToProps(state) {
  const {open} = state.dialogs;
  return {
    open
  }
}

export default connect(mapStateToProps)(FormDialog);