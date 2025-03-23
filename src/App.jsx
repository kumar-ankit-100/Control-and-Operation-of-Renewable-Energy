import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import PrivateRoute from './components/PrivateRoute';

// Layout Components
import Navbar from './components/layouts/Navbar';
import Footer from './components/layouts/Footer';

// Public Pages
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import Register from './pages/Register';
import Contact from './pages/Contact';
import ResourcesPage from './pages/Resources';

// Dashboard Pages - User
import UserDashboard from './pages/user/Dashboard';
import UserProfile from './pages/user/Profile';
import EnergyConsumption from './pages/user/EnergyConsumption';
import SmartDevices from './pages/user/SmartDevices';
import EnergyTips from './pages/user/EnergyTips';

// Dashboard Pages - Government
import GovDashboard from './pages/government/Dashboard';
import PolicyManagement from './pages/government/PolicyManagement';
import IncentivePrograms from './pages/government/IncentivePrograms';
import RegionalAnalytics from './pages/government/RegionalAnalytics';
import ConsumerData from './pages/government/ConsumerData';

// Dashboard Pages - Producers
import ProducerDashboard from './pages/producer/Dashboard';
import EnergyProduction from './pages/producer/EnergyProduction';
import StorageManagement from './pages/producer/StorageManagement';
import MarketInsights from './pages/producer/MarketInsights';
import SellEnergy from './pages/producer/SellEnergy';

// Dashboard Pages - Grid Operators
import GridDashboard from './pages/grid/Dashboard';
import LoadBalancing from './pages/grid/LoadBalancing';
import GridHealth from './pages/grid/GridHealth';
import PredictiveAnalytics from './pages/grid/PredictiveAnalytics';
import EmergencyResponse from './pages/grid/EmergencyResponse';

// Dashboard Pages - Operators
import OperatorDashboard from './pages/operator/Dashboard';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Navbar />
          <div className="container mx-auto px-4 py-8 min-h-screen">
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/resources" element={<ResourcesPage />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* User Routes */}
              <Route path="/user/*" element={<PrivateRoute userType="user" />}>
                <Route path="dashboard" element={<UserDashboard />} />
                <Route path="profile" element={<UserProfile />} />
                <Route path="consumption" element={<EnergyConsumption />} />
                <Route path="devices" element={<SmartDevices />} />
                <Route path="tips" element={<EnergyTips />} />
              </Route>

              {/* Government Routes */}
              <Route path="/government/*" element={<PrivateRoute userType="government" />}>
                <Route path="dashboard" element={<GovDashboard />} />
                <Route path="policies" element={<PolicyManagement />} />
                <Route path="incentives" element={<IncentivePrograms />} />
                <Route path="analytics" element={<RegionalAnalytics />} />
                <Route path="consumers" element={<ConsumerData />} />
              </Route>

              {/* Producer Routes */}
              <Route path="/producer/*" element={<PrivateRoute userType="producer" />}>
                <Route path="dashboard" element={<ProducerDashboard />} />
                <Route path="production" element={<EnergyProduction />} />
                <Route path="storage" element={<StorageManagement />} />
                <Route path="market" element={<MarketInsights />} />
                <Route path="sell" element={<SellEnergy />} />
              </Route>

              {/* Grid Operator Routes */}
              <Route path="/grid/*" element={<PrivateRoute userType="grid" />}>
                <Route path="dashboard" element={<GridDashboard />} />
                <Route path="balancing" element={<LoadBalancing />} />
                <Route path="health" element={<GridHealth />} />
                <Route path="analytics" element={<PredictiveAnalytics />} />
                <Route path="emergency" element={<EmergencyResponse />} />
              </Route>

              {/* Operator Routes */}
              <Route path="/operator/*" element={<PrivateRoute userType="operator" />}>
                <Route path="dashboard" element={<OperatorDashboard />} />
              </Route>
            </Routes>
          </div>
          <Footer />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;