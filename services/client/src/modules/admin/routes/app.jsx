import DashboardPage from "modules/admin/views/DashboardPage/DashboardPage";
import TableListPage from "modules/admin/views/TableListPage/TableListPage"
import OrdersPage from "modules/admin/views/OrdersPage/OrdersPage"

import {
  AttachMoney,
  ContentPaste,
  Dashboard,
} from "@material-ui/icons";

const appRoutes = [
  {
    path: "/admin/dashboard",
    sidebarName: "Dashboard",
    navbarName: "Dashboard",
    icon: Dashboard,
    component: DashboardPage
  },
  {
    path: "/admin/tables",
    sidebarName: "Table list",
    navbarName: "Table list",
    icon: ContentPaste,
    component: TableListPage
  },
  {
    path: "/admin/orders",
    sidebarName: "Orders",
    navbarName: "Orders",
    icon: AttachMoney,
    component: OrdersPage
  },
  {redirect: true, path: "/admin", to: "/admin/dashboard", navbarName: "Administration"}
];

export default appRoutes;
