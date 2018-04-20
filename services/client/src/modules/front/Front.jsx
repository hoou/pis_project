import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import classNames from 'classnames';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List from 'material-ui/List';
import Typography from 'material-ui/Typography';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import {NavLink, Redirect, Route, Switch} from "react-router-dom";
import {ListItem, ListItemIcon, ListItemText} from "material-ui";
import mainRoutes from "./routes/mainRoutes"
import userRoutes from "./routes/userRoutes"
import ProductDetailPage from "./views/ProductDetailPage/ProductDetailPage";

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
  }
});

class Front extends React.Component {
  state = {
    open: false
  };

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
    const {classes, theme} = this.props;

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
              <MenuIcon/>
            </IconButton>
            <Typography variant="title" color="inherit" noWrap className={classes.flex}>
              Title
            </Typography>
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
              {theme.direction === 'rtl' ? <ChevronRightIcon/> : <ChevronLeftIcon/>}
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
              {mainRoutes.map((prop, key) => {
                return <Route path={prop.path} component={prop.component} key={key}/>;
              })}
              {userRoutes.map((prop, key) => {
                return <Route path={prop.path} component={prop.component} key={key}/>;
              })}
              <Route path='/product/:id' component={ProductDetailPage}/>
              <Redirect from="/" to="/home"/>
            </Switch>
          </div>
        </main>
      </div>
    );
  }
}

Front.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, {withTheme: true})(Front);