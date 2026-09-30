import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import BuyerDashboard from './components/BuyerDashboard';
import FarmerDashboard from './components/FarmerDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/buyer-dashboard" element={<BuyerDashboard />} />
          <Route path="/farmer-dashboard" element={<FarmerDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
