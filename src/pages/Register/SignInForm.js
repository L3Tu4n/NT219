import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/SignIn.css";
import { EyeInvisibleOutlined, EyeTwoTone } from "@ant-design/icons";

function SignInForm() {
  const [form, setForm] = useState({
    UserName: "",
    Password: "",
  });

  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const { CCCD, Password } = form;
    if (CCCD === "079204123456" && Password === "admin") {
      navigate("/Admin");
    }
  };

  return (
    <form className="signin-form" onSubmit={handleSubmit}>
      <div className="signin">
        <label>
          CCCD<span style={{ color: "red" }}>*</span>
        </label>
        <input
          type="text"
          name="CCCD"
          placeholder="Nhập căn cước công dân"
          onChange={handleChange}
          className="input-signin-cccd"
          required
        />
      </div>

      <div className="password-container">
        <label>
          Mật khẩu<span style={{ color: "red" }}>*</span>
        </label>
        <input
          type={showPassword ? "text" : "password"}
          name="Password"
          placeholder="Nhập mật khẩu"
          onChange={handleChange}
          className="input-signin-password"
          required
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="toggle-password"
        >
          {showPassword ? (
            <EyeInvisibleOutlined />
          ) : (
            <EyeTwoTone twoToneColor="orangered" />
          )}
        </button>
      </div>

      <div className="signin-submit">
        <input type="submit" value="Đăng nhập" />
      </div>

      <div className="signup-link">
        Chưa có tài khoản?{" "}
        <a style={{ fontSize: 16 }} href="/SignUp">
          Đăng ký
        </a>
      </div>
    </form>
  );
}

export default SignInForm;
