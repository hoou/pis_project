import DashboardPage from "views/DashboardPage/DashboardPage";
import TableListPage from "views/TableListPage/TableListPage"
// import UserProfile from "views/UserProfile/UserProfile.jsx";
// import CategoriesPage from "views/CategoriesPage/CategoriesPage.jsx";
// import Typography from "views/Typography/Typography.jsx";
// import Icons from "views/Icons/Icons.jsx";
// import Maps from "views/Maps/Maps.jsx";
// import NotificationsPage from "views/Notifications/Notifications.jsx";

import {
  ContentPaste,
  Dashboard,
  // Person,
  // ContentPaste,
  // LibraryBooks,
  // BubbleChart,
  // LocationOn,
  // Notifications
} from "material-ui-icons";

const appRoutes = [
  {
    path: "/dashboard",
    sidebarName: "Dashboard",
    navbarName: "Dashboard",
    icon: Dashboard,
    component: DashboardPage
  },
  // {
  //   path: "/user",
  //   sidebarName: "User Profile",
  //   navbarName: "Profile",
  //   icon: Person,
  //   component: UserProfile
  // },
  {
    path: "/tables",
    sidebarName: "Table list",
    navbarName: "Table list",
    icon: ContentPaste,
    component: TableListPage
  },
  // {
  //   path: "/typography",
  //   sidebarName: "Typography",
  //   navbarName: "Typography",
  //   icon: LibraryBooks,
  //   component: Typography
  // },
  // {
  //   path: "/icons",
  //   sidebarName: "Icons",
  //   navbarName: "Icons",
  //   icon: BubbleChart,
  //   component: Icons
  // },
  // {
  //   path: "/maps",
  //   sidebarName: "Maps",
  //   navbarName: "Map",
  //   icon: LocationOn,
  //   component: Maps
  // },
  // {
  //   path: "/notifications",
  //   sidebarName: "Notifications",
  //   navbarName: "Notifications",
  //   icon: Notifications,
  //   component: NotificationsPage
  // },
  {redirect: true, path: "/", to: "/dashboard", navbarName: "Administration"}
];

export default appRoutes;
