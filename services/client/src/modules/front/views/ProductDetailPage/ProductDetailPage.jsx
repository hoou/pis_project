import React from "react";
import CircularIndeterminate from "modules/front/components/Progress/CircularIndeterminate/CircularIndeterminate";
import {Grid, Paper, Typography, withStyles} from "material-ui";
import ImageGridList from "modules/front/components/ImageGridList/ImageGridList";
import AddShoppingCartButton from "modules/front/components/ShoppingCart/AddShoppingCartButton/AddShoppingCartButton";

const styles = (theme) => ({
  paper: {
    padding: theme.spacing.unit * 2
  },
  button: {
    marginTop: 30,
    marginBottom: 10
  }
});

const ProductDetailPage = (props) => {
  const {product, classes} = props;
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
            <ImageGridList images={product['images']}/>
            <Typography variant="body1">
              {product['description']}
            </Typography>
            <div className={classes.button}>
              <AddShoppingCartButton raised id={product.id}/>
            </div>
          </Paper>
        </Grid>
      </Grid>
      :
      <CircularIndeterminate/>
  )
};

export default withStyles(styles)(ProductDetailPage);