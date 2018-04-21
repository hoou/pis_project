import React from 'react';
import {withStyles} from 'material-ui/styles';
import Stepper, {Step, StepLabel} from 'material-ui/Stepper';
import Button from 'material-ui/Button';
import Typography from 'material-ui/Typography';
import AddressForm from "modules/front/forms/AddressForm";
import {Paper} from "material-ui";
import {connect} from "react-redux";
import {checkoutActions} from "actions/checkout.actions";
import {submit} from "redux-form"
import ShippingAndPaymentForm from "modules/front/forms/ShippingAndPaymentForm";

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

function getStepContent(step) {
  switch (step) {
    case 0:
      return <AddressForm/>;
    case 1:
      return <ShippingAndPaymentForm/>;
    case 2:
      return 'This is the bit I really care about!';
    default:
      return 'Unknown step';
  }
}

class HorizontalLinearStepper extends React.Component {
  handleNext = () => {
    const {dispatch, activeStep} = this.props;

    if (activeStep === 0) {
      dispatch(submit("AddressForm"))
    } else if (activeStep === 1) {
      dispatch(submit("ShippingAndPaymentForm"))
    } else {
      dispatch(checkoutActions.next())
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
                {getStepContent(activeStep)}
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
  activeStep: state.checkout.activeStep
});
export default connect(mapStateToProps)(withStyles(styles)(HorizontalLinearStepper));