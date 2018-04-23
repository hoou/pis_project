import React from 'react';
import _ from "lodash"
import {Manager, Target, Popper} from "react-popper";
import {withStyles} from 'material-ui/styles';
import classNames from 'classnames';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List from 'material-ui/List';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton';
import {Menu, ChevronLeft, ChevronRight, ShoppingCart, Person, Email} from '@material-ui/icons';
import {Link, NavLink, Redirect, Route, Switch} from "react-router-dom";
import {
  Avatar,
  Badge, Button,
  ClickAwayListener, Grow,
  Hidden,
  ListItem,
  ListItemIcon,
  ListItemText,
  MenuItem,
  MenuList,
  Paper
} from "material-ui";
import mainRoutes from "./routes/mainRoutes"
import userRoutes from "./routes/userRoutes"
import ProductDetailPage from "./views/ProductDetailPage/ProductDetailPage";
import ShoppingCartPage from "./views/ShoppingCartPage/ShoppingCartPage";
import {shoppingCartActions} from "actions/shoppingCart.actions";
import CheckoutPage from "./views/CheckoutPage/CheckoutPage";
import {productsActions} from "actions/products.actions";
import ShopPage from "./views/ShopPage/ShopPage";
import HomePage from "./views/HomePage/HomePage";
import AlertDialog from "./components/Dialog/AlertDialog/AlertDialog";
import logo from "modules/front/assets/img/logo/whiteSide.png"
import {connect} from "react-redux";
import {categoriesActions} from "actions/categories.actions";
import authActions from "actions/auth.actions";
import LoginPage from "modules/front/views/LoginPage/LoginPage";
import {alertActions} from "../../actions/alert.actions";

const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
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
    flex: 1,
    display: "flex",
  },
  appBarIconButton: {
    marginRight: 20,
    color: '#fff'
  },
  logo: {
    height: 64
  },
  loginBtn: {
    color: "#fff"
  }
});

class Front extends React.Component {
  state = {
    open: false,
    menuOpen: false
  };

  constructor(props) {
    super(props);
    const {dispatch} = props;

    dispatch(authActions.checkLoggedIn(false));
    dispatch(shoppingCartActions.loadFromLocalStorage());
    dispatch(productsActions.getAll());
    dispatch(categoriesActions.getAll());
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

  handleLogout = () => {
    const {dispatch} = this.props;

    dispatch(authActions.logout());
    dispatch(alertActions.success("You were logged out"));
    this.setState({menuOpen: false});
  };

  handleDrawerOpen = () => {
    this.setState({open: true});
  };

  handleDrawerClose = () => {
    this.setState({open: false});
  };

  handleCloseMenu = () => {
    this.setState({menuOpen: false});
  };

  handleClickUserButton = () => {
    this.setState({menuOpen: !this.state.menuOpen});
  };

  render() {
    const {classes, loggedIn, theme, products, categories, cartItems, alert, user} = this.props;
    const {menuOpen} = this.state;

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
            <div className={classes.flex}>
              <img className={classes.logo} src={logo}/>
            </div>
            {loggedIn ? (
              <Manager style={{display: "inline-block"}}>
                <Target>
                  <IconButton
                    color="inherit"
                    aria-label="Person"
                    aria-owns={menuOpen ? "menu-list" : null}
                    aria-haspopup="true"
                    onClick={this.handleClickUserButton}
                    className={classes.buttonLink}
                  >
                    <Person className={classes.links}/>
                    <Hidden mdUp>
                      <p onClick={this.handleClickUserButton} className={classes.linkText}>
                        Profile
                      </p>
                    </Hidden>
                  </IconButton>
                </Target>
                <Popper
                  placement="bottom-start"
                  eventsEnabled={menuOpen}
                  className={
                    classNames({[classes.popperClose]: !menuOpen}) +
                    " " +
                    classes.pooperResponsive
                  }
                >
                  <ClickAwayListener onClickAway={this.handleCloseMenu}>
                    <Grow
                      in={menuOpen}
                      id="menu-list"
                      style={{transformOrigin: "0 0 0"}}
                    >
                      <Paper className={classes.dropdown}>
                        <div>
                          <List>
                            <ListItem>
                              <Avatar>
                                <Email/>
                              </Avatar>
                              <ListItemText>{user && user.email}</ListItemText>
                            </ListItem>
                          </List>
                          <MenuList role="menu">
                            <MenuItem
                              onClick={this.handleLogout}
                              className={classes.dropdownItem}
                            >
                              Logout
                            </MenuItem>
                          </MenuList>
                        </div>
                      </Paper>
                    </Grow>
                  </ClickAwayListener>
                </Popper>
              </Manager>
            ) : (
              <Link to="/login">
                <Button className={classes.loginBtn}>
                  Log in
                </Button>
              </Link>
            )}
            <Link to='/shopping-cart'>
              <IconButton
                color='inherit'
                className={classes.appBarIconButton}
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
            {loggedIn && (
              <div>
                <Divider/>
                {this.userRoutesListItems}
              </div>
            )}
          </List>
        </Drawer>
        <main className={classes.content}>
          <div>
            <Switch>
              <Route exact path='/home' render={() => <HomePage products={products}/>}/>
              <Route exact path='/login' component={LoginPage}/>
              <Route exact path='/shop' render={() => <ShopPage products={products} categories={categories}/>}/>
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
  categories: state.categories.items,
  loggedIn: state.auth.loggedIn,
  user: state.auth.user
});
export default connect(mapStateToProps)(withStyles(styles, {withTheme: true})(Front));
