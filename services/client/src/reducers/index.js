import {combineReducers} from "redux";

import {authReducer} from "./auth.reducer";
import {alertReducer} from "./alert.reducer"
import {categoriesReducer} from "./categories.reducer"
import {productsReducer} from "./products.reducer"
import {dialogsReducer} from "./dialogs.reducer";
import {reducer as formReducer} from 'redux-form'

const rootReducer = combineReducers({
  auth: authReducer,
  alert: alertReducer,
  dialogs: dialogsReducer,
  categories: categoriesReducer,
  products: productsReducer,
  form: formReducer
});

export default rootReducer;