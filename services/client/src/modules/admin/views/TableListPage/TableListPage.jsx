import React from "react";
import {Grid, withStyles} from "material-ui";
import _ from "lodash"

import {RegularCard, ItemGrid} from "modules/admin/components/index";
import {CategoriesTable} from "./CategoriesTable";
import FormDialog from "modules/admin/components/FormDialog/FormDialog";
import {dialogsActions} from "actions/dialogs.actions";
import CategoryForm from "modules/admin/forms/CategoryForm";
import {connect} from "react-redux";
import Button from "modules/admin/components/CustomButtons/Button";
import {ProductsTable} from "./ProductsTable";
import ProductForm from "modules/admin/forms/ProductForm";

const styles = theme => ({
  button: {
    margin: theme.spacing.unit,
  },
  leftIcon: {
    marginRight: theme.spacing.unit,
  },
  rightIcon: {
    marginLeft: theme.spacing.unit,
  },
  iconSmall: {
    fontSize: 20,
  },
});


const TableListPage = (props) => {
  const categoryForm = () => {
    const {edit, editId, categories} = props;
    return <CategoryForm
      dontRenderSubmit
      data={edit ? _.find(categories, o => o.id === editId) : null}
      id={editId}
    />
  };
  const productForm = () => {
    const {edit, editId, products} = props;
    return <ProductForm
      dontRenderSubmit
      data={edit ? _.find(products, o => o.id === editId) : null}
      id={editId}
    />
  };

  const handleClickAddNewCategory = () => props.dispatch(dialogsActions.showNew("category"));
  const handleClickAddNewProduct = () => props.dispatch(dialogsActions.showNew("product"));

  return (
    <Grid container>
      <ItemGrid xs={12} sm={12} md={12}>
        <RegularCard
          cardTitle="Categories"
          content={
            <CategoriesTable/>
          }
          footer={
            <Button color="primary" onClick={handleClickAddNewCategory}>Add new category</Button>
          }
        />
      </ItemGrid>
      <ItemGrid xs={12} sm={12} md={12}>
        <RegularCard
          cardTitle="Products"
          content={
            <ProductsTable/>
          }
          footer={
            <Button color="primary" onClick={handleClickAddNewProduct}>Add new product</Button>
          }
        />
      </ItemGrid>
      {props.form ? <FormDialog form={props.form === "category" ? categoryForm() : productForm()}/> : null}
    </Grid>
  )
};

const mapStateToProps = state => {
  const {categories, products} = state;
  const {edit, editId, form} = state.dialogs;
  return {
    edit, editId, categories: categories.items, products: products.items, form
  }
};

export default connect(mapStateToProps)(withStyles(styles)(TableListPage));