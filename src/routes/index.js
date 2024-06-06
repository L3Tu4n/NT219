import SignUp from "../pages/Register/SignUp.jsx";
import SignIn from "../pages/Register/SignIn.jsx";
import NotFoundPage from "../pages/NotFoundPage/NotFoundPage";
import Home from "../pages/Home/Home.jsx";

export const routes = [
  {
    path: "/",
    page: Home,
    isShowHeader: true,
  },
  {
    path: "/SignUp",
    page: SignUp,
    isShowHeader: false,
  },
  {
    path: "/SignIn",
    page: SignIn,
    isShowHeader: false,
  },
  {
    path: "*",
    page: NotFoundPage,
  },
];
