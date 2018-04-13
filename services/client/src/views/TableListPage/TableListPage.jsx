import React from "react";
import {Grid, withStyles} from "material-ui";

import {RegularCard, ItemGrid} from "components/index";
import {CategoriesTable} from "./CategoriesTable";
import FormDialog from "../../components/FormDialog/FormDialog";
import AddCategoryForm from "../../forms/AddCategoryForm";

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


const TableListPage = () => (
  <Grid container>
    <ItemGrid xs={12} sm={12} md={12}>
      <RegularCard
        cardTitle="Categories"
        content={
          <CategoriesTable/>
        }
        footer={
          <FormDialog title="Add new category" form={<AddCategoryForm dontRenderSubmit/>}/>
        }
      />
    </ItemGrid>
  </Grid>
);

export default withStyles(styles)(TableListPage);