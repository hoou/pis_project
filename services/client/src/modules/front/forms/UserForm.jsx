import React from 'react'
import {Field, reduxForm, submit} from 'redux-form'
import {Button, Grid, MenuItem, TextField, withStyles} from "material-ui";
import {connect} from "react-redux";
import {checkoutActions} from "actions/checkout.actions";
import MaskedInput from 'react-text-mask';
import {isPhoneNumber, isZipCode} from "helpers/strings";

const styles = {
  button: {
    marginTop: 20
  }
};

const validate = values => {
  const errors = {};
  const requiredFields = [];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });

  if (values["phone"] === "+42_ ___ ___ ___") {
    values["phone"] = null;
  }

  if (values["zipCode"] === "___ __") {
    values["zipCode"] = null;
  }

  if (values["phone"] && !isPhoneNumber(values['phone'])) {
    errors['phone'] = 'Must be in format +42(0|1) xxx xxx xxx';
  }

  if (values["zipCode"] && !isZipCode(values['zipCode'])) {
    errors['zipCode'] = 'Must be in format xxx xx';
  }

  return errors
};

class UserForm extends React.Component {
  constructor(props) {
    super(props);
  }

  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      Object.keys(data).forEach(key => {
        change(key, data[key]);
      });
    }
  }

  renderTextField = ({type, select, required, children, input, id, label, meta: {touched, error}}) => {
    return <TextField
      fullWidth={true}
      label={label}
      id={id}
      helperText={touched && !!error ? error : ''}
      error={touched && !!error}
      margin="normal"
      type={type}
      select={select}
      required={required}
      {...input}
    >
      {children}
    </TextField>
  };


  TextMaskPhone = (props) => {
    const {inputRef, ...other} = props;

    return (
      <MaskedInput
        {...other}
        ref={inputRef}
        mask={['+', '4', '2', /[0-1]/, ' ', /\d/, /\d/, /\d/, ' ', /\d/, /\d/, /\d/, ' ', /\d/, /\d/, /\d/]}
        placeholderChar={'_'}
        showMask
      />
    );
  };

  TextMaskZipCode = (props) => {
    const {inputRef, ...other} = props;

    return (
      <MaskedInput
        {...other}
        ref={inputRef}
        mask={[/\d/, /\d/, /\d/, ' ', /\d/, /\d/]}
        placeholderChar={'_'}
        showMask
      />
    );
  };

  renderPhone = ({input, label, id, required, meta: {touched, error}}) => {
    const isError = touched && !!error;
    return (
      <TextField
        fullWidth={true}
        label={label}
        id={id}
        helperText={isError ? error : 'Only +421 or +420'}
        error={isError}
        margin="normal"
        required={required}
        InputLabelProps={{shrink: true}}
        InputProps={{inputComponent: this.TextMaskPhone}}
        {...input}
      />
    )
  };

  renderZipCode = ({input, label, id, required, meta: {touched, error}}) => {
    const isError = touched && !!error;
    return (
      <TextField
        fullWidth={true}
        label={label}
        id={id}
        helperText={isError ? error : ''}
        error={isError}
        margin="normal"
        required={required}
        InputLabelProps={{shrink: true}}
        InputProps={{inputComponent: this.TextMaskZipCode}}
        {...input}
      />
    )
  };


  render() {
    const {classes, dispatch, handleSubmit} = this.props;

    return (
      <form onSubmit={handleSubmit}>
        <Grid container spacing={16}>
          <Grid item xs={12} sm={6}>
            <Field name="firstName" label="First name" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field name="lastName" label="Last name" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12}>
            <Grid container>
              <Grid item xs={12} sm={6}>
                <Field name="phone" label="Phone" component={this.renderPhone}/>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field name="street" label="Street" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field name="zipCode" label="ZIP code" component={this.renderZipCode}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field name="city" label="City" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field select name="country" label="Country" component={this.renderTextField}>
              <MenuItem value={1}>Slovakia</MenuItem>
              <MenuItem value={0}>Czech republic</MenuItem>
            </Field>
          </Grid>
        </Grid>
        <Button className={classes.button} variant="raised" color="primary"
                onClick={() => dispatch(submit("UserForm"))}>Update profile</Button>
      </form>
    )
  }
}

const form = 'UserForm';

export default reduxForm({
  form,
  validate
})
(connect()(withStyles(styles)(UserForm)))