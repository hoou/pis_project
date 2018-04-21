import React from "react";
import HorizontalLinearStepper from "modules/front/components/Stepper/HorizontalLinearStepper/HorizontalLinearStepper";
import {Grid, Typography} from "material-ui";

class CheckoutPage extends React.Component {
  render() {
    return (
      <Grid container justify="center">
        <Grid item xs={12}  md={8} lg={6}>
          <Typography variant="display1">Checkout</Typography>
          <HorizontalLinearStepper/>
        </Grid>
      </Grid>
    )
  }
}

export default CheckoutPage;