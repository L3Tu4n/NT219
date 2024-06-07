import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Typography, Button, Box } from '@mui/material';
import "../../styles/RorG.css";

function RorG() {
  return (
    <Container maxWidth="sm" className="rorg">
      <Box mt={4} mb={2}>
        <Typography variant="h4" component="h1" gutterBottom>
          Bạn Đã Có Giấy Đi Chợ Chưa?
        </Typography>
      </Box>
      <Box mb={2} display="flex" justifyContent="center">
        <Button variant="contained" color="primary" component={Link} to="/yes">
          Đã có giấy đi chợ
        </Button>
        
        <Button variant="contained" color="secondary" component={Link} to="/no">
          Chưa có giấy đi chợ
        </Button>
      </Box>
    </Container>
  );
}

export default RorG;
