import React from "react";
import Carousel from "modules/front/components/Carousel/Carousel";
import {Grid, Typography, withStyles} from "material-ui";
import ProductCard from "modules/front/components/ProductCard/ProductCard";
import {productsActions} from "actions/products.actions";
import {connect} from "react-redux";

const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: 140,
    width: 100,
  },
  control: {
    padding: theme.spacing.unit * 2,
  },
  carousel: {
    margin: theme.spacing.unit * 20
  }
});

class HomePage extends React.Component {
  constructor(props) {
    super(props);
    const {dispatch} = props;

    dispatch(productsActions.getAll());
  }

  render() {
    const {products} = this.props;

    return (
      <div>
        <Carousel className={this.props.classes.carousel}/>
        <Typography variant="display1" gutterBottom>
          Featured items
        </Typography>
        <Grid container className={this.props.classes.root} spacing={16}>
          {products.map((product) => (
            <Grid item xs={12} sm={6} md={4} lg={2} key={product['id']}>
              <ProductCard product={product}/>
            </Grid>
          ))}
        </Grid>
      </div>
    )
  }
}

export default connect(state => ({products: state.products.items}))(withStyles(styles)(HomePage));