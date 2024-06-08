import React, { useState } from 'react';
import { Table, Button, Tag, Typography, Modal, Input } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import '../../styles/request.css';

const Request = () => {
  const [data, setData] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');

  const handleDownload = (record) => {
    if (record.status === "Đã ký") {
      const filename = `market_pass_${record.key}.txt`;
      const content = `Market Pass ID: ${record.marketPassId}\nID Number: ${record.idNumber}\nFrom: ${record.from}\nTo: ${record.to}\nStatus: ${record.status}`;
  
      const element = document.createElement('a');
      const file = new Blob([content], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = filename;
      document.body.appendChild(element);
      element.click();
    } else {
      alert("Chỉ giấy đã ký mới có thể tải xuống");
    }
  };

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    const newData = {
      key: (data.length + 1).toString(),
      marketPassId: `MP00${data.length + 1}`,
      idNumber: "123456789",
      from,
      to,
      status: "Chưa ký",
    };

    setData([...data, newData]);
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const columns = [
    {
      title: "ID giấy đi chợ",
      dataIndex: "marketPassId",
      key: "marketPassId",
      width: 150,
    },
    {
      title: "Căn cước công dân",
      dataIndex: "idNumber",
      key: "idNumber",
      width: 180,
    },
    {
      title: "Di chuyển từ",
      dataIndex: "from",
      key: "from",
      width: 200,
    },
    {
      title: "Điểm đến",
      dataIndex: "to",
      key: "to",
      width: 200,
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
          onClick={() => handleDownload(record)}
          disabled={record.status === "Đã ký"}
          icon={<DownloadOutlined />}
        >
          Tải xuống
        </Button>
      ),
    },
  ];

  return (
    <div className="container">
      <Table
        columns={columns}
        dataSource={data}
        pagination={{ pageSize: 7 }}
        rowClassName={(record) =>
          record.status === "Đã ký" ? "signed-row" : ""
        }
        locale={{ emptyText: <Typography>No data</Typography> }}
      />
      <div className="request-button-container">
        <Button
          type="primary"
          onClick={showModal}
        >
          Xin giấy
        </Button>
        <Modal
          title={<Typography variant="h4" component="h1" gutterBottom className="request-title">YÊU CẦU CẤP GIẤY ĐI CHỢ</Typography>}
          visible={isModalVisible}
          onOk={handleOk}
          onCancel={handleCancel}
        >
          <div style={{ marginBottom: 16 }}>
            <Input
              placeholder="Di chuyển từ"
              value={from}
              onChange={(e) => setFrom(e.target.value)}
            />
          </div>
          <div style={{ marginBottom: 16 }}>
            <Input
              placeholder="Điểm đến"
              value={to}
              onChange={(e) => setTo(e.target.value)}
            />
          </div>
        </Modal>
      </div>
    </div>
  );
};

export default Request;
