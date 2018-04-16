import React from "react";
import EditTable from "components/Table/EditTable";
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import {dialogsActions} from "actions/dialogs.actions";
import _ from "lodash"

class ProductsTable extends React.Component {
  constructor(props) {
    super(props);

    this.props.dispatch(productsActions.getAll());

    this.handleRemove = this.handleRemove.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
  }

  handleRemove(id) {
    this.props.dispatch(productsActions.remove(id))
  }

  handleEdit(id) {
    this.props.dispatch(dialogsActions.showEdit("product", id))
  }

  render() {
    const {items} = this.props.products;
    let tableData = [];
    if (items) {
      /*
      [{id: 1, name: "Traktory"}, {id: 2, name: "Kultivatory"}]
        ===>
      [["1", "Traktory"], ["2", "Kultivatory"]]
       */

      tableData = _.map(items, item => _.map([..._.values(item)], item => {
        if (item) {
          if (item instanceof Object) {
            return item["name"];
          } else {
            return item.toString();
          }
        } else {
          return '';
        }
      }));

      // orderBy
      tableData = _.orderBy(tableData, item => _.toInteger(item[0]), "asc");
    }

    return (
      <EditTable
        tableHeaderColor="primary"
        tableHead={["#", "Name", "Description", "Price", "Category"]}
        tableData={tableData}
        handleRemove={this.handleRemove}
        handleEdit={this.handleEdit}
      />
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