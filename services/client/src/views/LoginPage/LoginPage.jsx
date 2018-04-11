import React from 'react';
import {connect} from 'react-redux';

import {userActions} from 'actions';
import LoginForm from "forms/LoginForm/LoginForm";

class LoginPage extends React.Component {

	constructor(props) {
		super(props);

		// reset login status
		this.props.dispatch(userActions.logout());

		// this.state = {
		// 	email: '',
		// 	password: '',
		// 	submitted: false
		// };

		// this.handleChange = this.handleChange.bind(this);
		// this.handleSubmit = this.handleSubmit.bind(this);
	}

	// handleChange(e) {
	// 	const {name, value} = e.target;
	// 	this.setState({[name]: value});
	// }
	//

	submit = values => {
		const {dispatch} = this.props;
		dispatch(userActions.login(values.email, values.password))
	};

	// handleSubmit(e) {
	// 	e.preventDefault();
	//
	// 	this.setState({submitted: true});
	// 	const {email, password} = this.state;
	// 	const {dispatch} = this.props;
	// 	if (email && password) {
	// 		dispatch(userActions.login(email, password));
	// 	}
	// }

	render() {
		const {loggingIn, error, errorMessage} = this.props;
		// const {email, password, submitted} = this.state;
		return (
			<div>
				<h2>Login</h2>
				<LoginForm onSubmit={this.submit} loggingIn={loggingIn}/>
				<p>{error ? errorMessage : ""}</p>
			</div>
		);
	}
}

function mapStateToProps(state) {
	const {loggingIn, error, errorMessage} = state.authentication;
	return {
		loggingIn, error, errorMessage
	};
}

const connectedLoginPage = connect(mapStateToProps)(LoginPage);
export {connectedLoginPage as LoginPage};