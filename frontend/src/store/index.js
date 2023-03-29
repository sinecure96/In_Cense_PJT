import { configureStore, combineReducers } from "@reduxjs/toolkit";
import { persistReducer, persistStore } from "redux-persist";
import storageSession from "redux-persist/lib/storage/session";
// import persistStore from 'redux-persist/es/persistStore';
import { articleReducers } from "./slice/articleSlice";
import { userReducers } from "./slice/userSlice";

// const customHistory = createBrowserHistory();

const rootReducer = combineReducers({
  articleReducers,
  userReducers,
});

const persistConfig = {
  key: "root",
  storage: storageSession, // 세션스토리지 사용
};

const store = configureStore({
  reducer: persistReducer(persistConfig, rootReducer),
});

export const persistor = persistStore(store);
export default store;