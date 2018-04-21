import React from "react"
import _ from "lodash";
import {Button, IconButton, Table, TableBody, TableCell, TableHead, TableRow, withStyles} from "material-ui";
import {dangerColor} from "modules/admin/assets/jss/material-dashboard-react";
import {Link} from "react-router-dom";
import {Delete} from "@material-ui/icons"
import {connect} from "react-redux";
import {shoppingCartActions} from "actions/shoppingCart.actions";

const styles = (theme) => ({
  table: {
    minWidth: 700,
  },
  tableCellProduct: {
    paddingLeft: 40
  },
  button: {
    margin: theme.spacing.unit,
    color: dangerColor
  },
  deleteCell: {
    maxWidth: 20
  }
});

class CustomTable extends React.Component {
  handleOnClickDelete = id => () => {
    const {dispatch} = this.props;

    dispatch(shoppingCartActions.remove(id))
  };

  render() {
    const {classes, items, products} = this.props;

    const countedItems = _.countBy(items);

    let sum = 0;

    return (
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell/>
            <TableCell className={classes.tableCellProduct}>Product</TableCell>
            <TableCell numeric>Count</TableCell>
            <TableCell numeric>Price per item</TableCell>
            <TableCell numeric>Price together</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {_.map(_.keys(countedItems), key => {
              const product = _.find(products, product => product['id'] === _.toInteger(key));
              const count = countedItems[key];
              if (product) {
                sum += count * product['price'];
              }
              return (
                product ?
                  <TableRow key={key}>
                    <TableCell className={classes.deleteCell}>
                      <IconButton onClick={this.handleOnClickDelete(product['id'])} className={classes.button}
                                  aria-label="Delete">
                        <Delete/>
                      </IconButton>
                    </TableCell>
                    <TableCell>
                      <Link to={"/product/" + key}>
                        <Button>
                          {product['name']}
                        </Button>
                      </Link>
                    </TableCell>
                    <TableCell numeric>{count}</TableCell>
                    <TableCell numeric>{product['price']}</TableCell>
                    <TableCell numeric>{count * product['price']}</TableCell>
                  </TableRow> : null
              )
            }
          )}
          <TableRow>
            <TableCell/>
            <TableCell/>
            <TableCell/>
            <TableCell/>
            <TableCell variant="head" numeric>
              {sum !== 0 ? "Sum: " + sum : null}
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    )
  }
}

const mapStateToProps = state => ({
  items: state.shoppingCart.items,
  products: state.products.items
});

export default connect(mapStateToProps)(withStyles(styles)(CustomTable));