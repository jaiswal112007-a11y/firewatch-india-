import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import LandingPage from './Landingpage';
import Dashboard from './Dashboard';
import Alerts from './Alerts';
import HotspotTable from './HotspotTable';
import './App.css';

function Navbar() {
  return (
    <nav className="navbar">
      <NavLink to="/" style={{textDecoration: 'none'}} className="nav-brand">
        🔥 FireWatch India
      </NavLink>
      <div className="nav-links">
        <NavLink to="/dashboard" className={({isActive}) => isActive ? 'active' : ''}>
          Dashboard
        </NavLink>
        <NavLink to="/alerts" className={({isActive}) => isActive ? 'active' : ''}>
          Alerts
        </NavLink>
        <NavLink to="/hotspots" className={({isActive}) => isActive ? 'active' : ''}>
          Hotspots
        </NavLink>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={
          <div className="app">
            <Navbar />
            <div className="page-content"><Dashboard /></div>
          </div>
        } />
        <Route path="/alerts" element={
          <div className="app">
            <Navbar />
            <div className="page-content"><Alerts /></div>
          </div>
        } />
        <Route path="/hotspots" element={
          <div className="app">
            <Navbar />
            <div className="page-content"><HotspotTable /></div>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;