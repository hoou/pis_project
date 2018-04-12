import React from 'react';
import {Route, Redirect} from 'react-router-dom';

export const PrivateRoute = ({component: Component, loggedIn, ...rest}) => (
  <Route {...rest} render={props => {
    let all = Object.assign({}, props, rest);
    return (
      loggedIn
        ? <Component {...all}/>
        : <Redirect to={{pathname: '/login', state: {from: props.location}}}/>
    );
  }
  }/>
);