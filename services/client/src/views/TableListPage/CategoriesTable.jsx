import React from "react";
import EditTable from "components/Table/EditTable";
import {connect} from "react-redux";
import {categoriesActions} from "actions/categories.actions";
import {dialogsActions} from "actions/dialogs.actions";
import _ from "lodash"

class CategoriesTable extends React.Component {
  constructor(props) {
    super(props);

    this.props.dispatch(categoriesActions.getAll());

    this.handleRemove = this.handleRemove.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
  }

  handleRemove(id) {
    this.props.dispatch(categoriesActions.remove(id))
  }

  handleEdit(id) {
    this.props.dispatch(dialogsActions.showEdit("category", id))
  }

  render() {
    const {items} = this.props.categories;
    let tableData = [];
    if (items) {
      /*
      [{id: 1, name: "Traktory"}, {id: 2, name: "Kultivatory"}]
        ===>
      [["1", "Traktory"], ["2", "Kultivatory"]]
       */
      tableData = _.map(items, item => _.map([..._.values(item)], item => item.toString()));

      // orderBy
      tableData = _.orderBy(tableData, item => _.toInteger(item[0]), "asc");
    }

    return (
      <EditTable
        tableHeaderColor="primary"
        tableHead={["#", "Name"]}
        tableData={tableData}
        handleRemove={this.handleRemove}
        handleEdit={this.handleEdit}
      />
    )
  }
}

function mapStateToProps(state) {
  return {
    categories: state.categories
  }
}

const connectedCategoriesTable = connect(mapStateToProps)(CategoriesTable);

export {connectedCategoriesTable as CategoriesTable};