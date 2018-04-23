import {combineReducers} from "redux";

import {authReducer} from "./auth.reducer";
import {alertReducer} from "./alert.reducer"
import {categoriesReducer} from "./categories.reducer"
import {productsReducer} from "./products.reducer"
import {ordersReducer} from "./orders.reducers"
import {dialogsReducer} from "./dialogs.reducer";
import {usersReducer} from "./users.reducer";
import {shoppingCartReducer} from "./shoppingCart.reducer";
import {checkoutReducer} from "./checkout.reducer";
import {reducer as formReducer} from 'redux-form'

const rootReducer = combineReducers({
  auth: authReducer,
  alert: alertReducer,
  users: usersReducer,
  dialogs: dialogsReducer,
  categories: categoriesReducer,
  products: productsReducer,
  orders: ordersReducer,
  checkout: checkoutReducer,
  shoppingCart: shoppingCartReducer,
  form: formReducer
});

export default rootReducer;