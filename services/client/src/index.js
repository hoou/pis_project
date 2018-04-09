import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import ProductsList from './components/ProductsList'

class App extends Component {
	constructor() {
		super();
		this.state = {
			products: []
		}
	}

	componentDidMount() {
		this.getProducts();
	}

	render() {
		return (
			<div className="container">
				<div className="row">
					<div className="col-md-4">
						<br/>
						<h1>All Products</h1>
						<hr/>
						<br/>
						<ProductsList products={this.state.products}/>
					</div>
				</div>
			</div>
		)
	}

	getProducts() {
		axios.get(`${process.env.REACT_APP_API_SERVICE_URL}/products`)
			.then((res) => {
				this.setState({products: res.data})
			})
			.catch((err) => {
				console.log(err);
			});
	}
}

ReactDOM.render(<App/>, document.getElementById('root'));
