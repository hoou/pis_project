import React from 'react'
import _ from "lodash"
import {Field, reduxForm} from 'redux-form'
import {Button, MenuItem, withStyles} from "material-ui";
import RegularButton from "modules/admin/components/CustomButtons/Button"
import PropTypes from "prop-types"
import CustomInput from "modules/admin/components/CustomInput/CustomInput";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import floatNormalizer from "modules/admin/forms/normalizers/float.normalizer";
import twoDecimalPlacesNormalizer from "./normalizers/twoDecimalPlaces.normalizer";
import greaterThan from "./normalizers/greaterOrEqualThan.normalizer";

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
};

class FieldFileInput extends React.Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);

    this.fileInput = React.createRef();
    this.clickFileInput = this.clickFileInput.bind(this);

    this.state = {
      file: null
    }
  }

  clickFileInput() {
    this.fileInput.current.click();
  }

  onChange(e) {
    const {input: {onChange}} = this.props;
    onChange(e.target.files[0]);

    this.setState({
      file: e.target.files[0].name
    })
  }

  render() {
    const {input} = this.props;
    const {file} = this.state;
    return (
      <div>
        <Button
          style={{marginRight: 5}}
          onClick={this.clickFileInput}
          variant="raised"
          color="primary"
        >
          Upload image
          <input
            ref={this.fileInput}
            type='file'
            accept='.jpg, .png, .jpeg'
            onChange={this.onChange}
            style={{display: 'none'}}
          />
        </Button>
        {file}
      </div>
    )
  }
}

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
      change("count", data["count"]);
    }
  }

  render() {
    const {classes, dontRenderSubmit, categories} = this.props;

    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <div>
          <Field required name="name" component={renderTextField} label="Name"/>
        </div>
        <div>
          <Field name="count" component={renderTextField} label="Count" type="number" required
                 normalize={greaterThan(0)}/>
        </div>
        <div>
          <Field name="description" component={renderTextField} label="Description"/>
        </div>
        <div>
          <Field required name="price" component={renderTextField} label="Price" type="number"
                 normalize={(val) => twoDecimalPlacesNormalizer(floatNormalizer(val))}/>
        </div>
        <div>
          <Field required name="category" label="Category" component={renderTextField} select>
            {categories.map(category => (
              <MenuItem key={category.id} value={category.id}>
                {category.name}
              </MenuItem>
            ))}
          </Field>
        </div>
        <div>
          <Field name="image" label="Image" component={FieldFileInput}/>
          {/*<Button*/}
          {/*variant="raised"*/}
          {/*component="label"*/}
          {/*color="primary">*/}
          {/*Upload*/}
          {/*<input type="file" style={{"display": "none"}} onChange={this.handleFileUploadChange}/>*/}
          {/*</Button>*/}
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