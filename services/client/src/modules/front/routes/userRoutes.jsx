import {
  Person
} from "@material-ui/icons";
import ProfilePage from "../views/ProfilePage/ProfilePage";

const userRoutes = [
  {
    path: "/profile",
    name: "Profile",
    icon: Person,
    component: ProfilePage
  },
];

export default userRoutes;
