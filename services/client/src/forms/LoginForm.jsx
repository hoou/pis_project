import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {withStyles} from "material-ui";
import RegularButton from "components/CustomButtons/Button"
import PropTypes from "prop-types"
import CustomInput from "../components/CustomInput/CustomInput";

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

// const asyncValidate = (values /*, dispatch */) => {
// 	return sleep(1000).then(() => {
// 		// simulate server latency
// 		if (['john', 'paul', 'george', 'ringo'].includes(values.email)) {
// 			throw {email: 'That email is taken'}
// 		}
// 	})
// };

const renderTextField = ({input, label, meta: {touched, error}, ...custom}) => {
//  <TextField label={label}
  //            error={touched && !!error}
  //           helperText={(touched && !!error) ? error : ''}
  //          {...input}
  //         {...custom}
  // />

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


  // classes,
  // formControlProps,
  // labelText,
  // id,
  // labelProps,
  // inputProps,
  // error,
  // success

};

let LoginForm = props => {
  const {handleSubmit, classes, loggingIn} = props;
  return (
    <form onSubmit={handleSubmit}>
      <div>
        {/*<Field name="email" component={renderTextField} label="Email"/>*/}
        <Field name="email" component={renderTextField} label="Email"/>
      </div>
      <div>
        <Field name="password" type="password" component={renderTextField} label="Password"/>
      </div>
      <div>
        <RegularButton variant="raised" color="primary" className={classes.button}
                       type="submit">{loggingIn ? 'Logging in...' : 'Log in'}</RegularButton>
      </div>
    </form>
  )
};

LoginForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default reduxForm({
  form: 'LoginForm',  // a unique identifier for this form
  validate
  // asyncValidate
})(
  withStyles(styles)(LoginForm)
)