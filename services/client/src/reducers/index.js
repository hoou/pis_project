import {combineReducers} from "redux";

import {authReducer} from "./auth.reducer";
import {alertReducer} from "./alert.reducer"
import {usersReducer} from "./users.reducer"
import {categoriesReducer} from "./categories.reducer"
import {dialogsReducer} from "./dialogs.reducer";
import {reducer as formReducer} from 'redux-form'

const rootReducer = combineReducers({
  auth: authReducer,
  alert: alertReducer,
  dialogs: dialogsReducer,
  users: usersReducer,
  categories: categoriesReducer,
  form: formReducer
});

export default rootReducer;