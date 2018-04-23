import React from "react";
import HorizontalLinearStepper from "modules/front/components/Stepper/HorizontalLinearStepper/HorizontalLinearStepper";
import {Grid, Typography} from "material-ui";
import _ from "lodash"
import {Redirect} from "react-router-dom";

const CheckoutPage = (props) => {
  const {products, cartItems, cartItemsLoadedFromCache} = props;
  return (
    cartItemsLoadedFromCache ? (
      _.size(cartItems) > 0 ?
        <Grid container justify="center">
          <Grid item xs={12} md={8} lg={6}>
            <Typography variant="display1">Checkout</Typography>
            <HorizontalLinearStepper products={products} cartItems={cartItems}/>
          </Grid>
        </Grid>
        :
        <Redirect to="/home"/>
    ) : null
  );
};


export default CheckoutPage;