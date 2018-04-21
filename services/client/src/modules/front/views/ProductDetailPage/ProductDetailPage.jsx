import React from "react";
import CircularIndeterminate from "modules/front/components/Progress/CircularIndeterminate/CircularIndeterminate";
import {Paper, Typography, withStyles} from "material-ui";
import ImageGridList from "modules/front/components/ImageGridList/ImageGridList";

const styles = (theme) => ({
  paper: {
    padding: theme.spacing.unit * 2
  }
});

const ProductDetailPage = (props) => {
  const {product, classes} = props;
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
};

export default withStyles(styles)(ProductDetailPage);