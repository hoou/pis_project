import React from "react";
import classNames from "classnames";
import {Manager, Target, Popper} from "react-popper";
import {
  withStyles,
  IconButton,
  MenuItem,
  MenuList,
  Grow,
  Paper,
  ClickAwayListener,
  Hidden
} from "material-ui";
import {Person, Notifications, Dashboard, Search} from "material-ui-icons";

import {CustomInput, IconButton as SearchButton} from "components";

import headerLinksStyle from "variables/styles/headerLinksStyle";
import authActions from "../../actions/auth.actions";

class HeaderLinks extends React.Component {
  state = {
    open: false,
    userDropdownOpen: false
  };

  handleClick = () => {
    this.setState({open: !this.state.open});
  };

  handleClose = () => {
    this.setState({open: false});
  };

  handleLogout = () => {
    this.setState({open: false});
    console.log('props', this.props);
    this.props.handleLogout();
  };

  render() {
    console.log(this.props);
    const {classes} = this.props;
    const {open} = this.state;
    return (
      <div>
        <CustomInput
          formControlProps={{
            className: classes.top + " " + classes.search
          }}
          inputProps={{
            placeholder: "Search",
            inputProps: {
              "aria-label": "Search"
            }
          }}
        />
        <SearchButton
          color="white"
          aria-label="edit"
          customClass={classes.top + " " + classes.searchButton}
        >
          <Search className={classes.searchIcon}/>
        </SearchButton>
        <Manager style={{display: "inline-block"}}>
          <Target>
            <IconButton
              color="inherit"
              aria-label="Person"
              aria-owns={open ? "menu-list" : null}
              aria-haspopup="true"
              onClick={this.handleClick}
              className={classes.buttonLink}
            >
              <Person className={classes.links}/>
              <Hidden mdUp>
                <p onClick={this.handleClick} className={classes.linkText}>
                  Profile
                </p>
              </Hidden>
            </IconButton>
          </Target>
          <Popper
            placement="bottom-start"
            eventsEnabled={open}
            className={
              classNames({[classes.popperClose]: !open}) +
              " " +
              classes.pooperResponsive
            }
          >
            <ClickAwayListener onClickAway={this.handleClose}>
              <Grow
                in={open}
                id="menu-list"
                style={{transformOrigin: "0 0 0"}}
              >
                <Paper className={classes.dropdown}>
                  <MenuList role="menu">
                    <MenuItem
                      onClick={this.handleLogout}
                      className={classes.dropdownItem}
                    >
                      Logout
                    </MenuItem>
                  </MenuList>
                </Paper>
              </Grow>
            </ClickAwayListener>
          </Popper>
        </Manager>
      </div>
    );
  }
}

export default withStyles(headerLinksStyle)(HeaderLinks);
