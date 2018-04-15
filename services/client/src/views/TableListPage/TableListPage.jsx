import React from "react";
import {Grid, withStyles} from "material-ui";
import _ from "lodash"

import {RegularCard, ItemGrid} from "components/index";
import {CategoriesTable} from "./CategoriesTable";
import FormDialog from "components/FormDialog/FormDialog";
import {dialogsActions} from "actions/dialogs.actions";
import CategoryForm from "forms/CategoryForm";
import {connect} from "react-redux";
import Button from "components/CustomButtons/Button";

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
  const {dispatch, edit, editId, categories} = props;

  const handleClickAddNewCategory = () => dispatch(dialogsActions.showNew("category"));

  return (
    <Grid container>
      <ItemGrid xs={12} sm={12} md={12}>
        <RegularCard
          cardTitle="Categories"
          content={
            <CategoriesTable/>
          }
          footer={
            <div>
              <Button color="primary" onClick={handleClickAddNewCategory}>Add new category</Button>
              <FormDialog form={
                <CategoryForm
                  dontRenderSubmit
                  data={edit ? _.find(categories, o => o.id === editId) : null}
                  id={editId}
                />
              }/>
            </div>
          }
        />
      </ItemGrid>
    </Grid>
  )
};

const mapStateToProps = state => {
  const {edit, editId} = state.dialogs;
  const {items} = state.categories;
  return {
    edit, editId, categories: items
  }
};

export default connect(mapStateToProps)(withStyles(styles)(TableListPage));