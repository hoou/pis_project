import {combineReducers} from 'redux';

import {authentication} from './authentication.reducer';
import {users} from './users.reducer';
import { reducer as formReducer } from 'redux-form'

const rootReducer = combineReducers({
	authentication,
	users,
	form: formReducer
});

export default rootReducer;