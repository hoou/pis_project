import React from "react";
import PropTypes from "prop-types";
import {Switch, Route, Redirect} from "react-router-dom";
// creates a beautiful scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import {withStyles} from "material-ui";

import {Header, Footer, Sidebar} from "components";

import appRoutes from "routes/app.jsx";

import appStyle from "variables/styles/appStyle.jsx";

import image from "assets/img/sidebar-3.jpg";
import logo from "assets/img/reactlogo.png";

const switchRoutes = (
  <Switch>
    {appRoutes.map((prop, key) => {
      if (prop.redirect)
        return <Redirect from={prop.path} to={prop.to} key={key}/>;
      return <Route path={prop.path} component={prop.component} key={key}/>;
    })}
  </Switch>
);

class Admin extends React.Component {
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
    const {classes, ...rest} = this.props;
    console.log('admin', this.props);
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
            <div className={classes.container}>{switchRoutes}</div>
          </div>
          <Footer/>
        </div>
      </div>
    );
  }
}

Admin.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(appStyle)(Admin);