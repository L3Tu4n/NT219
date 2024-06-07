import SignUp from "../pages/Register/SignUp.jsx";
import SignIn from "../pages/Register/SignIn.jsx";
import NotFoundPage from "../pages/NotFoundPage/NotFoundPage";
import Home from "../pages/Home/Home.jsx";
import Admin from "../pages/Admin/Admin.jsx";
import RorG from "../pages/RorG/RorG.jsx";
import Request from "../pages/RorG/no.jsx";
import Get from "../pages/RorG/yes.jsx";

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
    path: "/RorG",
    page: RorG,
    isShowHeader: false,
  },
  {
    path: "/no",
    page: Request,
  },
  {
    path: "/yes",
    page: Get,
  },
];
