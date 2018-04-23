import React from 'react'
import {Field, reduxForm, submit} from 'redux-form'
import {Button, MenuItem, TextField} from "material-ui";
import {connect} from "react-redux";

const validate = values => {
  const errors = {};
  const requiredFields = ['rating'];
  requiredFields.forEach(field => {
    if (!values[field]) {
      errors[field] = 'Required'
    }
  });

  return errors
};


class RatingForm extends React.Component {
  componentWillMount() {
    const {data, change} = this.props;

    if (data) {
      Object.keys(data).forEach(key => {
        change(key, data[key]);
      })
    }
  }

  renderTextField = ({type, select, required, children, input, id, label, meta: {touched, error}}) => {
    return <TextField
      fullWidth={true}
      label={label}
      id={id}
      helperText={touched && !!error ? error : ''}
      error={touched && !!error}
      margin="normal"
      type={type}
      select={select}
      required={required}
      {...input}
    >
      {children}
    </TextField>
  };

  render() {
    const {dispatch} = this.props;
    return (
      <form onSubmit={(e) => e.preventDefault()}>
        <Field select required name="rating" label="Rating" component={this.renderTextField}>
          <MenuItem value={1}>1</MenuItem>
          <MenuItem value={2}>2</MenuItem>
          <MenuItem value={3}>3</MenuItem>
          <MenuItem value={4}>4</MenuItem>
          <MenuItem value={5}>5</MenuItem>
        </Field>
        <Button
          variant="raised"
          color="primary"
          onClick={() => dispatch(submit("RatingForm"))}
        >
          Send rating
        </Button>
      </form>
    )
  }
}

const form = 'RatingForm';

export default reduxForm({
  form,
  validate
})
(connect()(RatingForm))