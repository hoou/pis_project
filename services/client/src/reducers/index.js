import {combineReducers} from "redux";

import {authReducer} from "./auth.reducer";
import {usersReducer} from "./users.reducer"
import {categoriesReducer} from "./categories.reducer"
import {reducer as formReducer} from 'redux-form'

const rootReducer = combineReducers({
  auth: authReducer,
  users: usersReducer,
  categories: categoriesReducer,
  form: formReducer
});

export default rootReducer;