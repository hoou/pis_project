import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {
  FormControlLabel, FormHelperText,
  FormLabel,
  Grid, Radio,
} from "material-ui";
import {connect} from "react-redux";
import {checkoutActions} from "actions/checkout.actions";
import {RadioGroup} from "redux-form-material-ui"

const validate = values => {
  const errors = {};
  const requiredFields = ['shipping', 'payment'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });

  return errors
};

function submit(values, dispatch) {
  dispatch(checkoutActions.submitShippingAndPayment(values));
  dispatch(checkoutActions.next());
}

class ShippingAndPaymentForm extends React.Component {
  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      Object.keys(data).forEach(key => {
        change(key, data[key]);
      })
    }
  }

  renderRadioGroup = ({children, required, label, meta: {touched, error}, ...props}) => {
    const isError = touched && !!error;
    return (
      <div>
        <FormLabel error={isError} required={required}>{label}</FormLabel>
        <RadioGroup {...props}>
          {children}
        </RadioGroup>
        <FormHelperText error={isError}>
          {isError ? error : ''}
        </FormHelperText>
      </div>
    );
  };

  render() {
    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <Grid container spacing={16}>
          <Grid item xs={12} sm={6}>

            <Field required name="shipping" label="Shipping option" component={this.renderRadioGroup}>
              <FormControlLabel value="personal" control={<Radio color="primary"/>} label="Personal collection"/>
              <FormControlLabel value="best" control={<Radio color="primary"/>} label="Best delivery"/>
              <FormControlLabel value="post" control={<Radio color="primary"/>} label="Post office"/>
            </Field>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Field required name="payment" label="Payment type" component={this.renderRadioGroup}>
              <FormControlLabel value="card" control={<Radio color="primary"/>} label="Credit/Debit card"/>
              <FormControlLabel value="bank" control={<Radio color="primary"/>} label="Bank transfer"/>
              <FormControlLabel value="cash" control={<Radio color="primary"/>} label="Cash on delivery"/>
            </Field>
          </Grid>
        </Grid>
      </form>
    )
  }
}

const form = 'ShippingAndPaymentForm';

export default reduxForm({
  form,
  onSubmit: submit,
  validate
})
(connect(state => ({data: state.checkout.shippingAndPayment}))(ShippingAndPaymentForm))