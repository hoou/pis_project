import {combineReducers} from "redux";

import {authReducer} from "./auth.reducer";
import {usersReducer} from "./users.reducer"
import {reducer as formReducer} from 'redux-form'

const rootReducer = combineReducers({
  auth: authReducer,
  users: usersReducer,
  form: formReducer
});

export default rootReducer;