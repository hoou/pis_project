import React from 'react';
import _ from "lodash"
import {withStyles} from 'material-ui/styles';
import classNames from 'classnames';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List from 'material-ui/List';
import Typography from 'material-ui/Typography';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton';
import {Menu, ChevronLeft, ChevronRight, ShoppingCart} from '@material-ui/icons';
import {Link, NavLink, Redirect, Route, Switch} from "react-router-dom";
import {Badge, ListItem, ListItemIcon, ListItemText} from "material-ui";
import mainRoutes from "./routes/mainRoutes"
import userRoutes from "./routes/userRoutes"
import ProductDetailPage from "./views/ProductDetailPage/ProductDetailPage";
import {connect} from "react-redux";
import ShoppingCartPage from "./views/ShoppingCartPage/ShoppingCartPage";
import {shoppingCartActions} from "actions/shoppingCart.actions";
import CheckoutPage from "./views/CheckoutPage/CheckoutPage";
import {productsActions} from "actions/products.actions";
import ShopPage from "./views/ShopPage/ShopPage";
import HomePage from "./views/HomePage/HomePage";
import AlertDialog from "./components/Dialog/AlertDialog/AlertDialog";

const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
    height: "100%",
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36,
  },
  hide: {
    display: 'none',
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    height: '100%',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing.unit * 7,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing.unit * 9,
    },
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    paddingTop: theme.spacing.unit * 10
  },
  listItem: {
    color: "blue",
    '&:hover': {
      color: "blue",
    },
  },
  flex: {
    flex: 1
  },
  shoppingCartIconButton: {
    marginRight: 20,
    color: '#fff'
  }
});

class Front extends React.Component {
  state = {
    open: false
  };

  constructor(props) {
    super(props);
    const {dispatch} = props;

    dispatch(shoppingCartActions.loadFromLocalStorage());
    dispatch(productsActions.getAll());
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const {cartItems} = this.props;
    localStorage.setItem('shoppingCartItems', JSON.stringify(cartItems));
  }

  mainRoutesListItems = (
    <div>
      {mainRoutes.map((prop, key) => {
        return (
          <NavLink
            to={prop.path}
            key={key}
          >
            <ListItem button className={this.props.classes.listItem}>
              <ListItemIcon>
                <prop.icon/>
              </ListItemIcon>
              <ListItemText primary={prop.name}/>
            </ListItem>
          </NavLink>
        )
      })}
    </div>
  );

  userRoutesListItems = (
    <div>
      {userRoutes.map((prop, key) => {
        return (
          <NavLink
            to={prop.path}
            key={key}
          >
            <ListItem button className={this.props.classes.listItem}>
              <ListItemIcon>
                <prop.icon/>
              </ListItemIcon>
              <ListItemText primary={prop.name}/>
            </ListItem>
          </NavLink>
        )
      })}
    </div>
  );

  handleDrawerOpen = () => {
    this.setState({open: true});
  };

  handleDrawerClose = () => {
    this.setState({open: false});
  };

  render() {
    const {classes, theme, products, cartItems, alert} = this.props;

    return (
      <div className={classes.root}>
        <AppBar
          position="absolute"
          className={classNames(classes.appBar, this.state.open && classes.appBarShift)}
        >
          <Toolbar disableGutters={!this.state.open}>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={this.handleDrawerOpen}
              className={classNames(classes.menuButton, this.state.open && classes.hide)}
            >
              <Menu/>
            </IconButton>
            <Typography variant="title" color="inherit" noWrap className={classes.flex}>
              Title
            </Typography>
            <Link to='/shopping-cart'>
              <IconButton
                color='inherit'
                className={classes.shoppingCartIconButton}
              >
                {
                  cartItems && cartItems.length > 0 ?
                    <Badge badgeContent={cartItems.length} color="error">
                      <ShoppingCart/>
                    </Badge>
                    :
                    <ShoppingCart/>
                }
              </IconButton>
            </Link>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          classes={{
            paper: classNames(classes.drawerPaper, !this.state.open && classes.drawerPaperClose),
          }}
          open={this.state.open}
        >
          <div className={classes.toolbar}>
            <IconButton onClick={this.handleDrawerClose}>
              {theme.direction === 'rtl' ? <ChevronRight/> : <ChevronLeft/>}
            </IconButton>
          </div>
          <Divider/>
          <List onClick={this.handleDrawerClose}>
            {this.mainRoutesListItems}
            <Divider/>
            {this.userRoutesListItems}
          </List>
        </Drawer>
        <main className={classes.content}>
          <div>
            <Switch>
              <Route exact path='/home' render={() => <HomePage products={products}/>}/>
              <Route exact path='/shop' component={ShopPage}/>
              {userRoutes.map((prop, key) => {
                return <Route path={prop.path} component={prop.component} key={key}/>;
              })}
              <Route
                exact
                path='/shopping-cart'
                render={() => <ShoppingCartPage products={products} items={cartItems}/>}
              />
              <Route exact path='/checkout' render={() => <CheckoutPage products={products} cartItems={cartItems}/>}/>
              <Route
                exact
                path='/product/:id'
                render={
                  (props) =>
                    <ProductDetailPage product={_.find(products, o => (o.id === _.toInteger(props.match.params.id)))}/>
                }
              />
              <Redirect from="/" to="/home"/>
            </Switch>
          </div>
        </main>
        {alert.message && <AlertDialog title={alert.type} content={alert.message}/>}
      </div>
    );
  }
}

const mapStateToProps = state => ({
  cartItems: state.shoppingCart.items,
  products: state.products.items,
  alert: state.alert,
});
export default connect(mapStateToProps)(withStyles(styles, {withTheme: true})(Front));
