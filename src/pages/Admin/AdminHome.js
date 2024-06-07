import React, { useState } from "react";
import { Table, Button, Tag } from "antd";
import "../../styles/AdminHome.css";

const columns = [
  {
    title: "ID giấy đi chợ",
    dataIndex: "marketPassId",
    key: "marketPassId",
    width: 150,
  },
  {
    title: "Tên",
    dataIndex: "name",
    key: "name",
    width: 200,
  },
  {
    title: "Căn cước công dân",
    dataIndex: "idNumber",
    key: "idNumber",
    width: 200,
  },
  {
    title: "Giới tính",
    dataIndex: "gender",
    key: "gender",
    width: 100,
  },
  {
    title: "Trạng thái",
    key: "status",
    dataIndex: "status",
    width: 100,
    render: (status) => (
      <Tag color={status === "Đã ký" ? "green" : "red"}>{status}</Tag>
    ),
  },
  {
    title: "Hành động",
    key: "action",
    width: 100,
    render: (_, record) => (
      <Button
        className="styled-button"
        onClick={() => record.onClick()}
        disabled={record.status === "Đã ký"}
      >
        {record.status === "Đã ký" ? "Đã ký" : "Ký"}
      </Button>
    ),
  },
];

const initialData = [
  {
    key: "1",
    marketPassId: "MP001",
    name: "Nguyễn Văn A",
    idNumber: "123456789",
    gender: "Nam",
    status: "Chưa ký",
  },
  {
    key: "2",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
  {
    key: "3",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
  {
    key: "4",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
  {
    key: "5",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
  {
    key: "6",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
  {
    key: "7",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
  {
    key: "8",
    marketPassId: "MP002",
    name: "Trần Thị B",
    idNumber: "987654321",
    gender: "Nữ",
    status: "Chưa ký",
  },
];

const AdminHome = () => {
  const [data, setData] = useState(initialData);

  const handleSign = (key) => {
    setData((prevData) =>
      prevData.map((item) =>
        item.key === key
          ? { ...item, status: item.status === "Chưa ký" ? "Đã ký" : "Chưa ký" }
          : item
      )
    );
  };

  const dataWithActions = data.map((item) => ({
    ...item,
    onClick: () => handleSign(item.key),
  }));

  return (
    <div className="container">
      <Table
        columns={columns}
        dataSource={dataWithActions}
        pagination={{ pageSize: 7 }}
        rowClassName={(record) =>
          record.status === "Đã ký" ? "signed-row" : ""
        }
      />
    </div>
  );
};

export default AdminHome;
