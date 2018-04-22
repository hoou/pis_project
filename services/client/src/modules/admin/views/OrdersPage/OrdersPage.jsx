import React from "react";
import {
  Button,
  List,
  ListItem,
  ListItemText,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  withStyles
} from "material-ui";
import {connect} from "react-redux";
import _ from "lodash"
import {ordersActions} from "actions/orders.actions";
import {Link} from "react-router-dom";
import FormDialog from "modules/admin/components/FormDialog/FormDialog";
import OrderStatusForm from "modules/admin/forms/OrderStatusForm";
import {dialogsActions} from "actions/dialogs.actions";

const styles = {
  listItem: {
    paddingLeft: 0
  },
  button: {
    marginLeft: 10
  }
};

class OrdersPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      data: null,
      id: null
    }
  }

  componentWillMount() {
    const {dispatch} = this.props;

    dispatch(ordersActions.getAll());
  }

  handleChangeStatusButtonClick = (id) => () => {
    const {dispatch, orders} = this.props;

    this.setState({
      data: {status: _.find(orders, o => o.id === id)["status"]},
      id: id
    });
    dispatch(dialogsActions.showEdit("order", id))
  };

  render() {
    const {orders, classes} = this.props;

    return (
      <div>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>Status</TableCell>
              <TableCell numeric>Total</TableCell>
              <TableCell>Items</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {_.map(orders, order => (
              <TableRow key={order["id"]}>
                <TableCell>{order["id"]}</TableCell>
                <TableCell>{order["status_name"]}</TableCell>
                <TableCell numeric>{order["total"]} EUR</TableCell>
                <TableCell>
                  <List>
                    {_.map(order["items"], item => (
                      <ListItem className={classes.listItem} key={item["id"]}>
                        <ListItemText>
                          {item["count"]}x
                          <Link to={"/product/" + item["product"]["id"]}>
                            <Button className={classes.button}>
                              {item["product"]["name"]}
                            </Button>
                          </Link>
                        </ListItemText>
                      </ListItem>
                    ))}
                  </List>
                </TableCell>
                <TableCell>
                  <Button onClick={this.handleChangeStatusButtonClick(order["id"])} color="primary" variant="raised">
                    Change status
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <FormDialog form={<OrderStatusForm data={this.state.data} id={this.state.id}/>}/>
      </div>
    )
  }
}

export default connect(state => ({orders: state.orders.items}))(withStyles(styles)(OrdersPage));