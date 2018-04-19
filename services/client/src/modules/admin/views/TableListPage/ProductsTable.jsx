import React from "react";
import EditTable from "modules/admin/components/Table/EditTable";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import {dialogsActions} from "actions/dialogs.actions";
import _ from "lodash"
import {FormControlLabel, Switch} from "material-ui";

class ProductsTable extends React.Component {
  constructor(props) {
    super(props);

    this.props.dispatch(productsActions.getAll());
    this.props.dispatch(productsActions.getAllDeleted());

    this.handleRemove = this.handleRemove.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
    this.handleRestore = this.handleRestore.bind(this);

    this.state = {
      checked_show_deleted_products: false
    }
  }

  handleChangeShowDeletedProductsSwitch = event => {
    this.setState({
      checked_show_deleted_products: event.target.checked
    })
  };

  handleRemove(id) {
    this.props.dispatch(productsActions.remove(id))
  }

  handleEdit(id) {
    this.props.dispatch(dialogsActions.showEdit("product", id))
  }

  handleRestore(id) {
    this.props.dispatch(productsActions.restore(id))
  }

  render() {
    let {items, deleted_items} = this.props.products;
    let tableData = [];
    let tableHead = ["#", "Name", "Count", "Description", "Price", "Category", "Image"];
    let items_to_show = [];

    items = _.map(items, item => ({deleted: false, data: item}));

    if (this.state.checked_show_deleted_products) {
      deleted_items = _.map(deleted_items, item => ({deleted: true, data: item}));
      items_to_show = _.concat(items, deleted_items);
    } else {
      items_to_show = items;
    }

    if (items_to_show) {
      console.log("items to show", items_to_show);
      /*
      [{id: 1, name: "Traktory"}, {id: 2, name: "Kultivatory"}]
        ===>
      [["1", "Traktory"], ["2", "Kultivatory"]]
       */
      tableData = _.map(items_to_show, item => ({
        deleted: item.deleted, data: _.map([..._.values(item.data)], item => {
          if (item != null) {
            if (item instanceof Object) {
              return item["name"] ? item["name"] : item["url"];
            } else {
              return item.toString();
            }
          } else {
            return '';
          }
        })
      }));

      // orderBy
      tableData = _.orderBy(tableData, item => _.toInteger(item.data[0]), "asc");
    }

    return (
      <div>
        <FormControlLabel
          control={
            <Switch
              checked={this.state.checked_show_deleted_products}
              onChange={this.handleChangeShowDeletedProductsSwitch}
              color="primary"
            />}
          label="Show deleted products"
        />

        <EditTable
          tableHeaderColor="primary"
          tableHead={tableHead}
          tableData={tableData}
          handleRemove={this.handleRemove}
          handleEdit={this.handleEdit}
          handleRestore={this.handleRestore}
        />
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    products: state.products
  }
}

const connectedProductsTable = connect(mapStateToProps)(ProductsTable);

export {connectedProductsTable as ProductsTable};