import React from "react";
import _ from "lodash"
import Carousel from "modules/front/components/Carousel/Carousel";
import {Grid, Typography, withStyles} from "material-ui";
import ProductCard from "modules/front/components/ProductCard/ProductCard";
import Brands from "./Brands";


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

const HomePage = (props) => {
  const {classes, products} = props;

  const filteredProducts = _.take(_.orderBy(products, 'id', 'desc'), 6);

  return (
    <div>
      <Carousel className={classes.carousel}/>
      <Brands/>
      <Typography variant="display1" gutterBottom>
        Featured items
      </Typography>
      <Grid container className={classes.root} spacing={16}>
        {_.map(filteredProducts, product => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={product['id']}>
            <ProductCard product={product}/>
          </Grid>
        ))}
      </Grid>
    </div>
  )
};

export default withStyles(styles)(HomePage);