import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';

function YesPage() {
  return (
    <Container maxWidth="sm">
      <Box mt={4} mb={2}>
        <Typography variant="h4" component="h1" gutterBottom>
          Giấy Đi Chợ
        </Typography>
      </Box>
      <Box mb={2} display="flex" justifyContent="flex-end">
        <Button variant="contained" color="primary" href="?" download>
          Tải xuống
        </Button>
        <Box ml={1}>
          <Button variant="contained" color="primary" onClick={() => window.print()}>
            In
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default YesPage;
