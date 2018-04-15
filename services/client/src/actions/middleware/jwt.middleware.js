import authActions from "../auth.actions";
import jwt_decode from "jwt-decode";

export const jwt = store => next => action => {
  const state = store.getState();

  if (state.auth && state.auth.tokens) {
    // decode jwt so that we know if and when it expires
    const tokenExpiration = jwt_decode(state.auth.tokens["access_token"])["exp"];

    const isExpired = ((new Date(parseInt(tokenExpiration, 10) * 1000)) - Date.now()) < 5000;

    if (isExpired) {
      return next(authActions.logout());
    }
  }

  return next(action);
};