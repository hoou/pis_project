import {createStore, applyMiddleware} from 'redux';
import thunkMiddleware from 'redux-thunk';
import {createLogger} from 'redux-logger';
import rootReducer from 'reducers';
import devToolsEnhancer from 'remote-redux-devtools';
import {jwt} from "actions/middleware/jwt.middleware"

const loggerMiddleware = createLogger();

export const store = createStore(
  rootReducer,
  applyMiddleware(
    jwt,
    // devToolsEnhancer,
    thunkMiddleware,
    // loggerMiddleware
  )
);