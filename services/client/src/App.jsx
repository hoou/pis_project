import React, {Component} from 'react';
import axios from 'axios';
import {Route, Switch} from 'react-router-dom'

import ProductsList from "./components/ProductsList";
import About from "./components/About";
import NavBar from "./components/Navbar";

class App extends Component {
	constructor() {
		super();
		this.state = {
			products: [],
			title: 'E-shop',
		};
	};

	componentDidMount() {
		this.getProducts();
	};

	getProducts() {
		axios.get(`${process.env.REACT_APP_API_SERVICE_URL}/products`)
			.then((res) => {
				this.setState({products: res.data});
			})
			.catch((err) => {
				console.log(err);
			});
	};

	render() {
		return (
			<div>
				<NavBar title={this.state.title}/>
				<div className="container">
					<div className="row">
						<div className="col-md-6">
							<br/>
							<Switch>
								<Route exact path='/' render={() => (
									<div>
										<h1>All Products</h1>
										<hr/>
										<br/>
										<ProductsList products={this.state.products}/>
									</div>
								)}/>
								<Route exact path='/about' component={About}/>
							</Switch>
						</div>
					</div>
				</div>
			</div>
		)
	};
}

export default App;