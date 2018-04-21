import React from "react";
import {IconButton, Paper, Table, TableBody, TableCell, TableHead, TableRow, withStyles} from "material-ui";
import {Delete} from "@material-ui/icons"
import {connect} from "react-redux";
import {productsActions} from "actions/products.actions";
import _ from "lodash"
import {Link} from "react-router-dom";
import {dangerColor} from "modules/admin/assets/jss/material-dashboard-react";
import {shoppingCartActions} from "../../../../actions/shoppingCart.actions";

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
  link: {
    color: 'rgba(0, 0, 0, 0.87)'
  },
  button: {
    margin: theme.spacing.unit,
    color: dangerColor
  },
  deleteCell: {
    maxWidth: 20
  }
});

class ShoppingCartPage extends React.Component {
  constructor(props) {
    super(props);
    const {dispatch} = props;

    dispatch(productsActions.getAll());
  }

  handleOnClickDelete = id => () => {
    const {dispatch} = this.props;

    dispatch(shoppingCartActions.remove(id))
  };

  render() {
    const {classes, products, items} = this.props;

    const countedItems = _.countBy(items);

    let sum = 0;

    return (
      <Paper className={classes.root}>
        <Table className={classes.table}>
          <TableHead>
            <TableRow>
              <TableCell/>
              <TableCell>Product</TableCell>
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
                        <Link className={classes.link} to={"/product/" + key}>
                          {product['name']}
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
      </Paper>
    );
  }
}

const mapStateToProps = state => ({
  items: state.shoppingCart.items,
  products: state.products.items
});
export default connect(mapStateToProps)(withStyles(styles)(ShoppingCartPage));