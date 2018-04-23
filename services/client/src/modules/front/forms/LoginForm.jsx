import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {Button, TextField, withStyles} from "material-ui";
import RegularButton from "modules/admin/components/CustomButtons/Button"

const styles = theme => ({
  button: {
    margin: theme.spacing.unit,
  },
  input: {
    display: 'none',
  },
});

const validate = values => {
  const errors = {};
  const requiredFields = ['email', 'password'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });
  if (values.email && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = 'Invalid email address'
  }
  return errors
};

const renderTextField = ({type, select, required, children, input, id, label, meta: {touched, error}}) => {
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

let LoginForm = props => {
  const {handleSubmit, classes} = props;
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <Field name="email" component={renderTextField} label="Email"/>
      </div>
      <div>
        <Field name="password" type="password" component={renderTextField} label="Password"/>
      </div>
      <div>
        <Button variant="raised" color="primary" className={classes.button} type="submit">
          Log in
        </Button>
      </div>
    </form>
  )
};

export default reduxForm({
  form: 'LoginForm',  // a unique identifier for this form
  validate
})(
  withStyles(styles)(LoginForm)
)