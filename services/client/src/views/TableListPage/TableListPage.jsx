import React from "react";
import {Grid, withStyles} from "material-ui";

import {RegularCard, ItemGrid} from "components/index";
import {CategoriesTable} from "./CategoriesTable";
import FormDialog from "components/FormDialog/FormDialog";
import {dialogsActions} from "actions/dialogs.actions";
import AddCategoryForm from "forms/AddCategoryForm";
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
  const handleOpen = () => props.dispatch(dialogsActions.open());

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
              <Button color="primary" onClick={handleOpen}>Add new category</Button>
              <FormDialog title="Add new category" form={<AddCategoryForm dontRenderSubmit/>}/>
            </div>
          }
        />
      </ItemGrid>
    </Grid>
  )
};

export default connect()(withStyles(styles)(TableListPage));