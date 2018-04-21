import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {Grid, MenuItem, TextField, withStyles} from "material-ui";
import {connect} from "react-redux";
import {checkoutActions} from "actions/checkout.actions";
import MaskedInput from 'react-text-mask';
import {isPhoneNumber, isZipCode} from "helpers/strings";

const styles = theme => ({});

const validate = values => {
  const errors = {};
  const requiredFields = ['firstName', 'lastName', 'street', 'city', 'country'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });

  if (!isPhoneNumber(values['phone'])) {
    errors['phone'] = 'Must be in format +42(0|1) xxx xxx xxx';
  }

  if (!isZipCode(values['zipCode'])) {
    errors['zipCode'] = 'Must be in format xxx xx';
  }

  return errors
};

function submit(values, dispatch, props) {
  dispatch(checkoutActions.submitAddress(values));
  dispatch(checkoutActions.next());
}

class AddressForm extends React.Component {
  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      Object.keys(data).forEach(key => {
        change(key, data[key]);
      })
    }
  }

  renderTextField = ({type, select, required, children, input, id, label, meta: {touched, error}, ...custom}) => {
    const {classes} = this.props;

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
    const {classes} = this.props;
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
    const {classes} = this.props;
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
    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <Grid container spacing={16}>
          <Grid item xs={12} sm={6}>
            <Field required name="firstName" label="First name" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field required name="lastName" label="Last name" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12}>
            <Grid container>
              <Grid item xs={12} sm={6}>
                <Field required name="phone" label="Phone" component={this.renderPhone}/>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field required name="street" label="Street" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field required name="zipCode" label="ZIP code" component={this.renderZipCode}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field required name="city" label="City" component={this.renderTextField}/>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field select required name="country" label="Country" component={this.renderTextField}>
              <MenuItem value="Slovakia">Slovakia</MenuItem>
              <MenuItem value="Czech republic">Czech republic</MenuItem>
            </Field>
          </Grid>
        </Grid>
      </form>
    )
  }
}

const form = 'AddressForm';

export default reduxForm({
  form,
  onSubmit: submit,
  validate
})
(connect(state => ({data: state.checkout.address}))(withStyles(styles)(AddressForm)))