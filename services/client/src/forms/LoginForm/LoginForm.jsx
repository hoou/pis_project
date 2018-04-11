import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {Button, TextField, withStyles} from "material-ui";
import PropTypes from "prop-types"

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

// const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// const asyncValidate = (values /*, dispatch */) => {
// 	return sleep(1000).then(() => {
// 		// simulate server latency
// 		if (['john', 'paul', 'george', 'ringo'].includes(values.email)) {
// 			throw {email: 'That email is taken'}
// 		}
// 	})
// };

const renderTextField = ({input, label, meta: {touched, error}, ...custom}) => (
	<TextField label={label}
			   error={touched && !!error}
			   helperText={(touched && !!error) ? error : ''}
			   {...input}
			   {...custom}
	/>
);

let LoginForm = props => {
	const {handleSubmit, classes, loggingIn} = props;
	return (
		<form onSubmit={handleSubmit}>
			<div>
				<Field name="email" component={renderTextField} label="Email"/>
			</div>
			<div>
				<Field name="password" type="password" component={renderTextField} label="Password"/>
			</div>
			<div>
				<Button variant="raised" color="primary" className={classes.button} type="submit">{loggingIn ? 'Logging in...' : 'Log in'}</Button>
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