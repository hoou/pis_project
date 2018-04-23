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
import _ from "lodash";
import {Link} from "react-router-dom";

const styles = {
  listItem: {
    paddingLeft: 0
  },
  button: {
    marginLeft: 10
  }
};

const UserOrdersTable = props => {
  const {classes, orders} = props;
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>#</TableCell>
          <TableCell>Status</TableCell>
          <TableCell numeric>Total</TableCell>
          <TableCell>Items</TableCell>
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
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
};

export default withStyles(styles)(UserOrdersTable);