import React from 'react'
import _ from "lodash"
import {Field, reduxForm} from 'redux-form'
import {MenuItem, withStyles} from "material-ui";
import RegularButton from "components/CustomButtons/Button"
import PropTypes from "prop-types"
import CustomInput from "components/CustomInput/CustomInput";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import floatNormalizer from "forms/normalizers/float.normalizer";
import twoDecimalPlacesNormalizer from "./normalizers/twoDecimalPlaces.normalizer";

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
  const requiredFields = ['name', 'price', 'category'];
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

  // console.log("custom", custom);
  // console.log("input", input);

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
  // formControlProps,-
  // labelText,
  // id,
  // labelProps,
  // inputProps,
  // error,
  // success

};

function submit(values, dispatch, props) {
  if (props.data) {
    dispatch(productsActions.update(props.id, _.mapKeys(values, (value, key) => key === "category" ? "category_id" : key)))
  } else {
    dispatch(productsActions.add(values["category"], _.omit(values, "category")));
  }
}

class ProductForm extends React.Component {
  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      change("name", data["name"]);
      change("price", data["price"]);
      change("description", data["description"]);
      change("category", data["category"]["id"]);
    }
  }

  render() {
    const {classes, dontRenderSubmit, categories} = this.props;

    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <Field name="name" component={renderTextField} label="Name"/>
        </div>
        <div>
          <Field name="price" component={renderTextField} label="Price" type="number"
                 normalize={(val) => twoDecimalPlacesNormalizer(floatNormalizer(val))}/>
        </div>
        <div>
          <Field name="description" component={renderTextField} label="Description"/>
        </div>
        <div>
          <Field name="category" label="Category" component={renderTextField} select>
            {categories.map(category => (
              <MenuItem key={category.id} value={category.id}>
                {category.name}
              </MenuItem>
            ))}
          </Field>
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

ProductForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

const form = 'ProductForm';

export default reduxForm({
  form,  // a unique identifier for this form
  onSubmit: submit,
  validate
  // asyncValidate
})
(connect((state) => ({categories: state.categories.items}))(withStyles(styles)(ProductForm)))