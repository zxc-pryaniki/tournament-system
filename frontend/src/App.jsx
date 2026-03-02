import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Login from './pages/Login'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        
        <Route path="/" element={
          <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Головна сторінка турніру</h1>
            <p>Ви успішно увійшли!</p>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;