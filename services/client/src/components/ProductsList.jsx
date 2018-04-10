import React from 'react';

const ProductsList = (props) => {
	return (
		<div>
			{
				props.products.map((product) => {
					return (
						<h4 key={product.id} className="well">
							{product.name}
						</h4>
					)
				})
			}
		</div>
	)
};

export default ProductsList;