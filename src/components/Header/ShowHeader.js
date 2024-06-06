import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logIn, logOut } from "../../redux/actions";
import { Link } from "react-router-dom";
import "../../styles/Header.css";
import { Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";

const ShowHeader = () => {
  const navigate = useNavigate();
  var isLoggedIn = useSelector((state) => state.user.isLoggedIn);
  const username = useSelector((state) => state.user.username);
  const dispatch = useDispatch();

  const [dropdownVisible, setDropdownVisible] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    const username = localStorage.getItem("username");
    if (isLoggedIn) {
      dispatch(logIn(username));
    }
  }, []);

  const handleLogOut = () => {
    handleNormalLogOut();
  };

  const handleNormalLogOut = () => {
    dispatch(logOut());
    localStorage.setItem("isLoggedIn", "false");
    localStorage.removeItem("username");
    navigate("/");
  };

  useEffect(() => {
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => {
      window.removeEventListener("resize", checkMobile);
    };
  });

  const [isMobile, setIsMobile] = useState(false);
  const checkMobile = () => {
    setIsMobile(window.innerWidth <= 768);
  };

  return (
    <header className="header">
      <div className="desktop" style={{ display: "flex" }}>
        <div className="logo">
          <Link className="logo-link" to="/">
            Giấy đi chợ
          </Link>
        </div>
        <div className="options">
          <div className="actions">
            {isLoggedIn ? (
              <div className="user-dropdown" ref={dropdownRef}>
                <button
                  className="user-button"
                  onClick={() => setDropdownVisible(!dropdownVisible)}
                >
                  <Avatar size="small" icon={<UserOutlined />} /> {username}
                </button>
                {dropdownVisible && (
                  <div
                    className={`user-dropdown-content ${
                      dropdownVisible ? "show" : ""
                    }`}
                  >
                    <button onClick={handleLogOut}>Đăng xuất</button>
                  </div>
                )}
              </div>
            ) : (
              <button className="auth-button">
                <Link to="/SignIn">Đăng nhập | Đăng ký</Link>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default ShowHeader;
