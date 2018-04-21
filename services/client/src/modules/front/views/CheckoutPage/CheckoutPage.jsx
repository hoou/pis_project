import React from "react";
import HorizontalLinearStepper from "modules/front/components/Stepper/HorizontalLinearStepper/HorizontalLinearStepper";
import {Grid, Typography} from "material-ui";

const CheckoutPage = (props) => {
  const {products, cartItems} = props;
  return (
    <Grid container justify="center">
      <Grid item xs={12} md={8} lg={6}>
        <Typography variant="display1">Checkout</Typography>
        <HorizontalLinearStepper products={products} cartItems={cartItems}/>
      </Grid>
    </Grid>
  )
};


export default CheckoutPage;