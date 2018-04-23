import React from "react";
import CircularIndeterminate from "modules/front/components/Progress/CircularIndeterminate/CircularIndeterminate";
import {Grid, Paper, Typography, withStyles} from "material-ui";
import ImageGridList from "modules/front/components/ImageGridList/ImageGridList";
import AddShoppingCartButton from "modules/front/components/ShoppingCart/AddShoppingCartButton/AddShoppingCartButton";
import RatingForm from "modules/front/forms/RatingForm";
import {connect} from "react-redux";
import Rating from "./Rating";
import {productsActions} from "actions/products.actions";
import _ from "lodash"

const styles = (theme) => ({
  paper: {
    padding: theme.spacing.unit * 2
  },
  button: {
    marginTop: 30,
    marginBottom: 10
  }
});

class ProductDetailPage extends React.Component {
  handleSubmitRating = (values) => {
    const {dispatch, product} = this.props;

    dispatch(productsActions.postRating(product.id, values))
  };

  render() {
    const {product, classes, loggedIn, checkedLoggedIn, ratings, gotStatus, user} = this.props;

    const didIRate = checkedLoggedIn && loggedIn && gotStatus
      ? _.find(ratings, o => o["user"]["id"] === user["id"]) !== undefined
      : false;

    return (
      product ?
        <Grid container justify="center">
          <Grid item xs={12} sm={6}>
            <Paper className={classes.paper}>
              <Typography variant="headline">
                {product['name']}
              </Typography>
              <Typography variant="subheading">
                {product['price']} EUR
              </Typography>
              <Rating product={product}/>
              <ImageGridList images={product['images']}/>
              <Typography variant="body1">
                {product['description']}
              </Typography>
              <div className={classes.button}>
                <AddShoppingCartButton raised id={product.id}/>
              </div>
              {checkedLoggedIn && loggedIn && !didIRate && <RatingForm onSubmit={this.handleSubmitRating}/>}
            </Paper>
          </Grid>
        </Grid>
        :
        <CircularIndeterminate/>
    )
  }
}

const mapStateToProps = state => ({
  ratings: state.products.ratingsByProduct,
  loggedIn: state.auth.loggedIn,
  checkedLoggedIn: state.auth.checkedLoggedIn,
  user: state.auth.user,
  gotStatus: state.auth.gotStatus
});
export default connect(mapStateToProps)(withStyles(styles)(ProductDetailPage));