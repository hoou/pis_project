import React from 'react';
import Button from 'material-ui/Button';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from 'material-ui/Dialog';
import {connect} from "react-redux";
import {alertActions} from "actions/alert.actions";
import {Error} from "@material-ui/icons";

class AlertDialog extends React.Component {
  handleClose = () => {
    const {dispatch} = this.props;
    dispatch(alertActions.clear());
  };

  render() {
    const {title, content, open} = this.props;
    return (
      <div>
        <Dialog
          open={open}
          onClose={this.handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {title === "success" ? "Success" : <div>Error <Error color="error"/></div>}
          </DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {content}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary" autoFocus>
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default connect(state => ({open: state.alert.openDialog}))(AlertDialog);