import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {Button, TextField, withStyles} from "material-ui";

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
  const requiredFields = ['email', 'password', 'password2'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });
  if (values.email && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = 'Invalid email address'
  }

  if (values['password'] && values['password'].length < 6) {
    errors.password = 'Password must be at least 6 characters long';
  }

  if (values['password'] && values['password2'] && values['password'] !== values['password2']) {
    errors.password2 = 'Passwords must be the same';
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

let RegisterForm = props => {
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
        <Field name="password2" type="password" component={renderTextField} label="Password again"/>
      </div>
      <div>
        <Button variant="raised" color="primary" className={classes.button} type="submit">
          Register
        </Button>
      </div>
    </form>
  )
};

export default reduxForm({
  form: 'RegisterForm',  // a unique identifier for this form
  validate
})(
  withStyles(styles)(RegisterForm)
)