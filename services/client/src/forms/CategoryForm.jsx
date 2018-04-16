import React from 'react'
import {Field, reduxForm} from 'redux-form'
import {withStyles} from "material-ui";
import RegularButton from "components/CustomButtons/Button"
import PropTypes from "prop-types"
import CustomInput from "components/CustomInput/CustomInput";
import {connect} from "react-redux";
import {categoriesActions} from "actions/categories.actions";

const styles = theme => ({
  button: {
    margin: theme.spacing.unit,
  },
  input: {
    display: 'none',
  },
});

const validate = values => {
  const errors = {};
  const requiredFields = ['name'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });
  return errors
};

// const asyncValidate = (values /*, dispatch */) => {
// 	return sleep(1000).then(() => {
// 		// simulate server latency
// 		if (['john', 'paul', 'george', 'ringo'].includes(values.email)) {
// 			throw {email: 'That email is taken'}
// 		}
// 	})
// };

const renderTextField = ({input, label, meta: {touched, error}, ...custom}) => {
//  <TextField label={label}
  //            error={touched && !!error}
  //           helperText={(touched && !!error) ? error : ''}
  //          {...input}
  //         {...custom}
  // />

  return <CustomInput
    labelText={label}
    formControlProps={{
      fullWidth: true
    }}
    error={touched && !!error}
    errorMessage={error}
    inputProps={input}
    {...custom}
  />


  // classes,
  // formControlProps,
  // labelText,
  // id,
  // labelProps,
  // inputProps,
  // error,
  // success

};

function submit(values, dispatch, props) {
  if (props.data) {
    dispatch(categoriesActions.update(props.id, values))
  } else {
    dispatch(categoriesActions.add(values.name));
  }
}

class CategoryForm extends React.Component {
  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      change("name", data.name)
    }
  }

  render() {
    const {classes, dontRenderSubmit} = this.props;

    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <Field required name="name" component={renderTextField} label="Name"/>
        </div>
        <div>
          {dontRenderSubmit
            ? null
            : (
              <RegularButton variant="raised" color="primary" className={classes.button} type="submit">
                Send
              </RegularButton>
            )
          }
        </div>
      </form>
    )
  }
}

CategoryForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

const form = 'CategoryForm';

export default reduxForm({
  form,  // a unique identifier for this form
  onSubmit: submit,
  validate
  // asyncValidate
})
(connect()(withStyles(styles)(CategoryForm)))