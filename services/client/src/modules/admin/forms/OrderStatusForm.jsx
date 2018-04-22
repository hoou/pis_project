import React from 'react'
import {Field, reduxForm} from 'redux-form'
import CustomInput from "modules/admin/components/CustomInput/CustomInput";
import {MenuItem, withStyles} from "material-ui";
import {connect} from "react-redux";
import {ordersActions} from "../../../actions/orders.actions";

const styles = {};

const validate = values => {
  const errors = {};
  const requiredFields = ['status'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });
  return errors;
};

const renderTextField = ({input, label, meta: {touched, error}, ...custom}) => {
  return <CustomInput
    labelText={label}
    formControlProps={{
      fullWidth: true
    }}
    error={touched && !!error}
    errorMessage={error}
    inputProps={input}
    {...custom}
  />
};

function submit(values, dispatch, props) {
  dispatch(ordersActions.updateStatus(props.id, values["status"]))
}

class OrderStatusForm extends React.Component {
  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      change("status", data["status"]);
    }
  }

  render() {
    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <Field select name="status" component={renderTextField} label="Status">
            <MenuItem value={0}>pending</MenuItem>
            <MenuItem value={1}>awaiting payment</MenuItem>
            <MenuItem value={2}>awaiting shipment</MenuItem>
            <MenuItem value={3}>completed</MenuItem>
            <MenuItem value={4}>cancelled</MenuItem>
          </Field>
        </div>
      </form>
    )
  }
}

const form = 'OrderStatusForm';

export default reduxForm({
  form,  // a unique identifier for this form
  onSubmit: submit,
  validate,

})(
  connect()(withStyles(styles)(OrderStatusForm))
);