import React from 'react';
import _ from "lodash";
import {withStyles} from 'material-ui/styles';
import Stepper, {Step, StepLabel} from 'material-ui/Stepper';
import Button from 'material-ui/Button';
import Typography from 'material-ui/Typography';
import AddressForm from "modules/front/forms/AddressForm";
import {Paper} from "material-ui";
import {connect} from "react-redux";
import {checkoutActions} from "actions/checkout.actions";
import {ordersActions} from "actions/orders.actions";
import {submit} from "redux-form"
import ShippingAndPaymentForm from "modules/front/forms/ShippingAndPaymentForm";
import Summary from "modules/front/views/CheckoutPage/Summary";

const styles = theme => ({
  root: {
    width: '90%',
  },
  buttons: {
    float: "right"
  },
  button: {
    marginRight: theme.spacing.unit,
  },
  instructions: {
    marginTop: theme.spacing.unit,
    marginBottom: theme.spacing.unit,
  },
  stepper: {
    background: "none"
  },
  stepContent: {
    padding: 30,
    minHeight: 400,
    marginBottom: 30
  }
});

function getSteps() {
  return ['Address', 'Shipping and payment', 'Summary'];
}

class HorizontalLinearStepper extends React.Component {
  componentDidMount() {
    const {dispatch} = this.props;
    dispatch(checkoutActions.loadFromLocalStorage());
  }

  handleNext = () => {
    const {dispatch, activeStep, cartItems, address} = this.props;
    const countedCartItems = _.countBy(cartItems);

    if (activeStep === 0) {
      dispatch(submit("AddressForm"))
    } else if (activeStep === 1) {
      dispatch(submit("ShippingAndPaymentForm"))
    } else if (activeStep === 2) {
      const orderItems = _.map(
        _.keys(countedCartItems),
        key => ({"product_id": _.toInteger(key), "count": countedCartItems[key]})
      );
      const deliveryAddress = _.mapKeys(address, (value, key) => _.snakeCase(key));
      deliveryAddress["phone"] = deliveryAddress["phone"].replace(/\s/g, "");
      deliveryAddress["zip_code"] = deliveryAddress["zip_code"].replace(/\s/g, "");

      dispatch(ordersActions.add(orderItems, deliveryAddress));
    }
  };

  handleBack = () => {
    const {dispatch} = this.props;

    dispatch(checkoutActions.back())
  };

  handleReset = () => {
    const {dispatch} = this.props;

    dispatch(checkoutActions.reset())
  };

  getStepContent = step => {
    const {products, address, cartItems, shippingAndPayment} = this.props;

    switch (step) {
      case 0:
        return <AddressForm address={address}/>;
      case 1:
        return <ShippingAndPaymentForm/>;
      case 2:
        return (
          <Summary
            products={products}
            cartItems={cartItems}
            address={address}
            shipping={shippingAndPayment["shipping"]}
            payment={shippingAndPayment["payment"]}
          />
        );
      default:
        return 'Unknown step';
    }
  };

  render() {
    const {classes, activeStep} = this.props;
    const steps = getSteps();

    return (
      <div className={classes.root}>
        <Stepper className={classes.stepper} activeStep={activeStep}>
          {steps.map(label => {
            const props = {};
            const labelProps = {};
            return (
              <Step key={label} {...props}>
                <StepLabel {...labelProps}>{label}</StepLabel>
              </Step>
            );
          })}
        </Stepper>
        <div>
          {activeStep === steps.length ? (
            <div>
              <Typography className={classes.instructions}>
                All steps completed - you&quot;re finished
              </Typography>
              <Button onClick={this.handleReset} className={classes.button}>
                Reset
              </Button>
            </div>
          ) : (
            <div>
              <Paper className={classes.stepContent}>
                {this.getStepContent(activeStep)}
              </Paper>
              <div className={classes.buttons}>
                <Button
                  disabled={activeStep === 0}
                  onClick={this.handleBack}
                  className={classes.button}
                >
                  Back
                </Button>
                <Button
                  variant="raised"
                  color="primary"
                  onClick={this.handleNext}
                  className={classes.button}
                >
                  {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  activeStep: state.checkout.activeStep,
  address: state.checkout.address,
  shippingAndPayment: state.checkout.shippingAndPayment,
});
export default connect(mapStateToProps)(withStyles(styles)(HorizontalLinearStepper));
