import React from "react";
import PropTypes from "prop-types";
import {Switch, Route, Redirect} from "react-router-dom";
// creates a beautiful scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import {withStyles} from "material-ui";

import {Header, Footer, Sidebar} from "modules/admin/components/index";

import appRoutes from "modules/admin/routes/app.jsx";

import appStyle from "modules/admin/assets/jss/material-dashboard-react/appStyle";

import image from "modules/admin/assets/img/sidebar-3.jpg";
import logo from "modules/admin/assets/img/reactlogo.png";
import {connect} from "react-redux";
import SnackbarContent from "modules/admin/components/Snackbar/SnackbarContent";

const switchRoutes = (
  <Switch>
    {appRoutes.map((prop, key) => {
      if (prop.redirect)
        return <Redirect from={prop.path} to={prop.to} key={key}/>;
      return <Route path={prop.path} component={prop.component} key={key}/>;
    })}
  </Switch>
);

class AdminLayout extends React.Component {
  state = {
    mobileOpen: false
  };

  handleDrawerToggle = () => {
    this.setState({mobileOpen: !this.state.mobileOpen});
  };

  componentDidMount() {
    if (navigator.platform.indexOf('Win') > -1) {
      // eslint-disable-next-line
      const ps = new PerfectScrollbar(this.refs.mainPanel);
    }
  }

  componentDidUpdate() {
    this.refs.mainPanel.scrollTop = 0;
  }

  render() {
    const {classes, alert, ...rest} = this.props;
    return (
      <div className={classes.wrapper}>
        <Sidebar
          routes={appRoutes}
          logoText={"Creative Tim"}
          logo={logo}
          image={image}
          handleDrawerToggle={this.handleDrawerToggle}
          open={this.state.mobileOpen}
          color="blue"
          {...rest}
        />
        <div className={classes.mainPanel} ref="mainPanel">
          <Header
            routes={appRoutes}
            handleDrawerToggle={this.handleDrawerToggle}
            handleLogout={this.props.handleLogout}
            {...rest}
          />
          <div className={classes.content}>
            {alert.message &&
              <SnackbarContent
                        message={alert.message}
                        color={alert.type}
                      />
            }
            <div className={classes.container}>{switchRoutes}</div>
          </div>
          <Footer/>
        </div>
      </div>
    );
  }
}

AdminLayout.propTypes = {
  classes: PropTypes.object.isRequired
};

function mapStateToProps(state) {
  const {alert} = state;
  return {
    alert
  };
}

const connectedAdminLayout = connect(mapStateToProps)(withStyles(appStyle)(AdminLayout));
export {connectedAdminLayout as AdminLayout}