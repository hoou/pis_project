import React from "react";
import {withStyles, TextField} from "material-ui";
import PropTypes from "prop-types";

import customInputStyle from "variables/styles/customInputStyle";

function CustomInput({...props}) {
  const {
    // classes,
    // formControlProps,
    labelText,
    id,
    // labelProps,
    inputProps,
    error,
    errorMessage,
    // success,
    type
  } = props;

  return (
    <TextField
      label={labelText}
      id={id}
      helperText={error ? errorMessage : ''}
      error={error}
      margin="normal"
      type={type}
      fullWidth={true}
      {...inputProps}
    />

  );
}

CustomInput.propTypes = {
  // classes: PropTypes.object.isRequired,
  labelText: PropTypes.node,
  // labelProps: PropTypes.object,
  id: PropTypes.string,
  inputProps: PropTypes.object,
  // formControlProps: PropTypes.object,
  error: PropTypes.bool,
  errorMessage: PropTypes.string,
  // success: PropTypes.bool
};

export default withStyles(customInputStyle)(CustomInput);
