import React from 'react';
import {Router, Route} from 'react-router-dom';
import {connect} from 'react-redux';

import {history} from 'helpers';
import {PrivateRoute} from 'routes/PrivateRoute';
// import { HomePage } from '../HomePage';
import {LoginPage} from 'views/LoginPage';
import Admin from "containers/Admin/Admin"

class App extends React.Component {
	render() {
		return (
			<div className="jumbotron">
				<div className="container">
					<div className="col-sm-8 col-sm-offset-2">
						<Router history={history}>
							<div>
								<PrivateRoute exact path="/" component={Admin}/>
								<Route path="/login" component={LoginPage}/>
							</div>
						</Router>
					</div>
				</div>
			</div>
		);
	}
}

function mapStateToProps(state) {
	const {alert} = state;
	return {
		alert
	};
}

const connectedApp = connect(mapStateToProps)(App);
export {connectedApp as App};