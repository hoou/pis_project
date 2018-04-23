import React from "react";
import _ from "lodash";
import {
  FormControl, FormControlLabel,
  Grid,
  MenuItem,
  Paper, Radio,
  RadioGroup,
  TextField,
  Typography,
  withStyles
} from "material-ui";
import ProductCard from "modules/front/components/ProductCard/ProductCard";

const styles = {
  root: {
    padding: 50,
    minHeight: 300
  },
  headline: {
    marginBottom: 20
  },
  display: {
    marginBottom: 20
  },
  grid: {
    marginTop: 20
  },
  paper: {
    padding: 50
  }
};

class ShopPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      search: '',
      category: -1,
      orderBy: 'name',
      ascDesc: 'asc'
    }
  }

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  render() {
    const {classes, products, categories} = this.props;

    // filter by name
    let filteredProducts = _.filter(products, o => _.includes(_.lowerCase(o.name), _.lowerCase(this.state.search)));

    // filter by category
    if (this.state.category > 0) {
      filteredProducts = _.filter(filteredProducts, o => o["category"]["id"] === this.state.category)
    }

    // order
    filteredProducts = _.orderBy(filteredProducts, this.state.orderBy, this.state.ascDesc);

    return (
      <div className={classes.root}>
        <Typography className={classes.display} variant="display1">Shop</Typography>
        <Paper className={classes.paper}>
          <Grid container spacing={40}>
            <Grid item xs={12} sm={6}>
              <Grid container>
                <Grid item xs={12} lg={8}>
                  <Typography className={classes.headline} variant="headline">Filter</Typography>
                  <TextField
                    fullWidth={true}
                    id="select-category"
                    select
                    label="Category"
                    value={this.state.category}
                    onChange={this.handleChange('category')}
                  >
                    <MenuItem value={-1}>
                      <em>All</em>
                    </MenuItem>
                    {_.map(categories, category => (
                      <MenuItem key={category["id"]} value={category["id"]}>
                        {category["name"]}
                      </MenuItem>
                    ))}
                  </TextField>
                  <TextField
                    fullWidth={true}
                    id="search"
                    label="Search"
                    value={this.state.search}
                    onChange={this.handleChange('search')}
                  />
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Grid container>
                <Grid item xs={12}>
                  <Typography className={classes.headline} variant="headline">Order by</Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <FormControl component="fieldset">
                    <RadioGroup
                      aria-label="order by"
                      name="orderBy"
                      value={this.state.orderBy}
                      onChange={this.handleChange('orderBy')}
                    >
                      <FormControlLabel value="name" control={<Radio color="primary"/>} label="Name"/>
                      <FormControlLabel value="price" control={<Radio color="primary"/>} label="Price"/>
                    </RadioGroup>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <FormControl component="fieldset">
                    <RadioGroup
                      aria-label="asc/desc"
                      name="ascDesc"
                      value={this.state.ascDesc}
                      onChange={this.handleChange('ascDesc')}
                    >
                      <FormControlLabel value="asc" control={<Radio color="primary"/>} label="Ascending"/>
                      <FormControlLabel value="desc" control={<Radio color="primary"/>} label="Descending"/>
                    </RadioGroup>
                  </FormControl>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Paper>
        <Grid container className={classes.grid} spacing={16}>
          {_.map(filteredProducts, product => (
            <Grid item xs={12} sm={6} md={4} lg={2} key={product['id']}>
              <ProductCard product={product}/>
            </Grid>
          ))}
        </Grid>
      </div>
    )
  }
}

export default withStyles(styles)(ShopPage);