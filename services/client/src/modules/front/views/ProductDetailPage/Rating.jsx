import React from "react";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import _ from "lodash";

class Ratings extends React.Component {
  componentWillMount() {
    const {dispatch, product} = this.props;
    dispatch(productsActions.getRatings(product.id))
  }

  render() {
    const {ratings} = this.props;

    const justRatings = _.map(ratings, rating => rating["rating"]);

    return (
      <div>average rating: {justRatings.length > 0 ? _.mean(justRatings) : "no ratings yet"}</div>
    )
  }
}

export default connect(state => ({ratings: state.products.ratingsByProduct}))(Ratings);