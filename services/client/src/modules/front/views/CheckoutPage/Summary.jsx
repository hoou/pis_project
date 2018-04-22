import React from "react"
import {
  Grid,
  List,
  ListItem,
  ListItemText,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  withStyles
} from "material-ui";
import _ from "lodash";

const styles = () => ({
  listItem: {
    padding: 0
  },
  typographyBody1: {
    padding: 8,
    paddingLeft: 0
  }
});

const Summary = (props) => {
  const {address, classes, products, cartItems, shipping, payment} = props;
  const countedCartItems = _.countBy(cartItems);

  let sum = 0;

  return (
    <div>
      <Typography variant="headline">Products</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Product</TableCell>
            <TableCell numeric>Count</TableCell>
            <TableCell numeric>Price per item</TableCell>
            <TableCell numeric>Price together</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {_.map(_.keys(countedCartItems), key => {
            const product = _.find(products, product => product['id'] === _.toInteger(key));
            const count = countedCartItems[key];
            if (product) {
              sum += count * product['price'];
            }
            return (
              <TableRow key={key}>
                <TableCell>{product['name']}</TableCell>
                <TableCell numeric>{count}</TableCell>
                <TableCell numeric>{product['price']}</TableCell>
                <TableCell numeric>{count * product['price']}</TableCell>
              </TableRow>
            )
          })}
          <TableRow>
            <TableCell/>
            <TableCell/>
            <TableCell/>
            <TableCell variant="head" numeric>{sum !== 0 ? "Sum: " + sum : null}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <Grid container>
        <Grid item xs={12} sm={6}>
          <Typography variant="headline">Address</Typography>
          <List>
            {_.map(_.keys(address), key => (
              <ListItem key={key} className={classes.listItem}>
                <ListItemText>{address[key]}</ListItemText>
              </ListItem>
            ))}
          </List>
        </Grid>
        <Grid item xs={12} sm={6}>
          <div>
            <Typography variant="headline">Shipping</Typography>
            <Typography className={classes.typographyBody1} variant="body1">{shipping}</Typography>
          </div>
          <div>
            <Typography variant="headline">Payment</Typography>
            <Typography className={classes.typographyBody1} variant="body1">{payment}</Typography>
          </div>
        </Grid>
      </Grid>
    </div>
  );
};

export default withStyles(styles)(Summary);