import SignUp from "../pages/Register/SignUp.jsx";
import SignIn from "../pages/Register/SignIn.jsx";
import NotFoundPage from "../pages/NotFoundPage/NotFoundPage";
import Home from "../pages/Home/Home.jsx";
import Admin from "../pages/Admin/Admin.jsx";
import Request from "../pages/RequestGet/Request.jsx"

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
    path: "/Admin",
    page: Admin,
    isShowHeader: true,
  },
  {
    path: "*",
    page: NotFoundPage,
  },
  {
    path: "/Request",
    page: Request,
    isShowHeader: true,
  },
];
