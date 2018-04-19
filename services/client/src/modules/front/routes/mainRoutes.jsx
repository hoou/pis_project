import HomePage from "modules/front/views/HomePage/HomePage";
import ShopPage from "modules/front/views/ShopPage/ShopPage";

import {
  Home,
  Shop
} from "@material-ui/icons";

const mainRoutes = [
  {
    path: "/home",
    name: "Home",
    icon: Home,
    component: HomePage
  },
  {
    path: "/shop",
    name: "Shop",
    icon: Shop,
    component: ShopPage
  },
];

export default mainRoutes;
