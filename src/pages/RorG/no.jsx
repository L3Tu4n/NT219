import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Dialog, DialogTitle, DialogContent, DialogActions, Box } from '@mui/material';
import "../../styles/no.css";

function NoPage() {
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');
  const [idCard, setIdCard] = useState('');
  const [reason, setReason] = useState('');
  const [area, setArea] = useState('');
  const [open, setOpen] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Request submitted:', { name, address, phone, idCard, reason, area });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Yêu Cầu Cấp Giấy Đi Chợ
      </Typography>
      <form onSubmit={handleSubmit}>
        <Box mb={2}>
          <TextField
            label="Họ và tên"
            variant="outlined"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </Box>
        <Box mb={2}>
          <TextField
            label="Địa chỉ"
            variant="outlined"
            fullWidth
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
          />
        </Box>
        <Box mb={2}>
          <TextField
            label="Số điện thoại"
            variant="outlined"
            fullWidth
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </Box>
        <Box mb={2}>
          <TextField
            label="Số căn cước"
            variant="outlined"
            fullWidth
            value={idCard}
            onChange={(e) => setIdCard(e.target.value)}
            required
          />
        </Box>
        <Box mb={2}>
          <TextField
            label="Lý do ra đường"
            variant="outlined"
            fullWidth
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            required
          />
        </Box>
        <Box mb={2}>
          <TextField
            label="Khu vực di chuyển"
            variant="outlined"
            fullWidth
            value={area}
            onChange={(e) => setArea(e.target.value)}
            required
          />
        </Box>
        <Box mt={2}>
          <Button variant="contained" color="primary" type="submit" fullWidth>
            Gửi Yêu Cầu
          </Button>
        </Box>
      </form>

      {/* Hộp thoại thông báo */}
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Yêu cầu của bạn đã được chấp nhận</DialogTitle>
        <DialogContent>
          <Typography>Yêu cầu của bạn đã được chấp nhận. Vui lòng chờ đợi!</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary" autoFocus>
            Đóng
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default NoPage;
