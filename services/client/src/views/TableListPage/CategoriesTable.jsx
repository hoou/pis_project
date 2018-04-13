import React from "react";
import Table from "components/Table/Table";
import {connect} from "react-redux";
import {categoriesActions} from "actions/categories.actions";
import _ from "lodash"

class CategoriesTable extends React.Component {
  constructor(props) {
    super(props);

    this.props.dispatch(categoriesActions.getAll())
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
      let mappedItems = _.mapValues(
        {items},
        currentArray => _.map(_.map(currentArray, obj => _.mapValues(obj, val => val.toString())), _.values)
      );
      tableData = mappedItems.items
    }

    return (
      <Table
        tableHeaderColor="primary"
        tableHead={["ID", "Name"]}
        tableData={tableData}
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