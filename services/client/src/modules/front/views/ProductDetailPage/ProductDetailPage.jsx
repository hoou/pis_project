import React from "react";
import {connect} from "react-redux";
import CircularIndeterminate from "modules/front/components/Progress/CircularIndeterminate/CircularIndeterminate";
import {productsActions} from "actions/products.actions";
import {Paper, Typography, withStyles} from "material-ui";
import ImageGridList from "modules/front/components/ImageGridList/ImageGridList";

const styles = (theme) => ({
  paper: {
    padding: theme.spacing.unit * 2
  }
});

class ProductDetailPage extends React.Component {
  constructor(props) {
    super(props);

    props.dispatch(productsActions.get(props.match.params.id))
  }

  render() {
    const {product, classes} = this.props;
    return (
      product ?
        <Paper className={classes.paper}>
          <Typography variant="headline">
            {product['name']}
          </Typography>
          <Typography variant="subheading">
            {product['price']} EUR
          </Typography>
          <ImageGridList images={product['images']}/>
          <Typography variant="body1">
            {product['description']}
          </Typography>
        </Paper>
        :
        <CircularIndeterminate/>
    )
  }
}


const mapStateToProps = state => (
  {product: state.products.detail}
);


export default connect(mapStateToProps)(withStyles(styles)(ProductDetailPage));