import React, { useState } from "react";
import "../../styles/SignUp.css";
import { EyeInvisibleOutlined, EyeTwoTone } from "@ant-design/icons";

function SignUpForm() {
  const [form, setForm] = useState({
    UserName: "",
    Email: "",
    Password: "",
    confirmPassword: "",
    CCCD: "",
    FirstAndLastName: "",
    Address: "",
    Gender: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <form className="signup-form">
      <div className="signup">
        <label>
          CCCD<span style={{ color: "red" }}>*</span>
        </label>
        <input
          type="text"
          name="CCCD"
          placeholder="Nhập căn cước công dân"
          onChange={handleChange}
          className="input-signup-cccd"
          required
        />
      </div>

      <div className="signup">
        <label>
          Họ và tên<span style={{ color: "red" }}>*</span>
        </label>
        <input
          type="text"
          name="FirstAndLastName"
          placeholder="Nhập họ và tên"
          onChange={handleChange}
          className="input-first-and-last-name"
          required
        />
      </div>

      <div className="signup">
        <label>
          Địa chỉ<span style={{ color: "red" }}>*</span>
        </label>
        <input
          type="text"
          name="Address"
          placeholder="Nhập địa chỉ"
          onChange={handleChange}
          className="input-signup-address"
          required
        />
      </div>

      <div className="signup">
        <label>
          Giới tính<span style={{ color: "red" }}>*</span>
        </label>
        <div className="gender-container">
          <div className="custom-radio">
            <input
              type="radio"
              id="male"
              name="Gender"
              value="Nam"
              checked={form.Gender === "Nam"}
              onChange={handleChange}
            />
            <label for="male" className="custom-radio-label">
              Nam
            </label>
          </div>
          <div className="custom-radio">
            <input
              type="radio"
              id="female"
              name="Gender"
              value="Nữ"
              checked={form.Gender === "Nữ"}
              onChange={handleChange}
            />
            <label for="female" className="custom-radio-label">
              Nữ
            </label>
          </div>
        </div>
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
          className="input-signup-password"
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

      <label className="password-container">
        <label>
          Xác nhận lại mật khẩu<span style={{ color: "red" }}>*</span>
        </label>
        <input
          type={showConfirmPassword ? "text" : "password"}
          name="confirmPassword"
          placeholder="Nhập lại mật khẩu"
          onChange={handleChange}
          className="input-signup-password"
          required
        />
        <button
          type="button"
          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
          className="toggle-password"
        >
          {showConfirmPassword ? (
            <EyeInvisibleOutlined />
          ) : (
            <EyeTwoTone twoToneColor="orangered" />
          )}
        </button>
      </label>

      <div className="agreement">
        <input type="checkbox" required />
        <span>
          Tôi đồng ý với{" "}
          <a href="https://nplaw.vn/quy-dinh-cua-phap-luat-ve-bao-mat-thong-tin-ca-nhan.html">
            Điều khoản sử dụng
          </a>{" "}
          và{" "}
          <a href="https://nplaw.vn/quy-dinh-cua-phap-luat-ve-bao-mat-thong-tin-ca-nhan.html">
            Chính sách bảo mật
          </a>{" "}
          của Nhà Nước
        </span>
      </div>

      <div className="signup-submit">
        <input type="submit" value="Tiếp tục" />
      </div>

      <div className="login-link">
        Đã có tài khoản? <a href="/SignIn">Đăng nhập</a>
      </div>
    </form>
  );
}

export default SignUpForm;
