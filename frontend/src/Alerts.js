import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [chronic, setChronic] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAlerts = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/alerts');
      setAlerts(res.data.alerts);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchChronic = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/alerts/chronic');
      setChronic(res.data.chronic_sources);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAlerts();
    fetchChronic();
  }, []);

  if (loading) return <p style={{color:'#aaa', padding:'20px'}}>Loading alerts...</p>;

  return (
    <div>
      <h2 className="page-title">🚨 Active Alerts</h2>

      {/* High Priority Alerts */}
      <h3 style={{color:'#FF4500', marginBottom:'15px'}}>
        Industrial Fire & Gas Flare Alerts ({alerts.length})
      </h3>

      {alerts.length === 0 ? (
        <p style={{color:'#aaa'}}>No active alerts right now.</p>
      ) : (
        <div className="alert-list">
          {alerts.map((a) => (
            <div
              key={a.id}
              className={`alert-card ${a.priority === 'HIGH' ? 'high' : 'medium'}`}
            >
              <div className="alert-info">
                <h4>🔥 {a.fire_type}</h4>
                <p>📍 Lat: {a.latitude?.toFixed(3)}, Lon: {a.longitude?.toFixed(3)}</p>
                <p>⚡ FRP: {a.frp} MW &nbsp;|&nbsp; 🛰 {a.satellite} &nbsp;|&nbsp; 📅 {a.acq_date}</p>
                <p>🎯 Confidence: {a.confidence_score ? (a.confidence_score * 100).toFixed(0) : 0}%</p>
              </div>
              <div style={{display:'flex', flexDirection:'column', alignItems:'flex-end', gap:'8px'}}>
                <span className={`alert-badge ${a.priority === 'HIGH' ? 'badge-high' : 'badge-medium'}`}>
                  {a.priority}
                </span>
                {a.is_chronic === 'yes' && (
                  <span className="alert-badge badge-chronic">CHRONIC</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Chronic Sources */}
      <h3 style={{color:'#FF00FF', margin:'30px 0 15px'}}>
        ♾ Chronic Fire Sources ({chronic.length})
      </h3>

      {chronic.length === 0 ? (
        <p style={{color:'#aaa'}}>No chronic sources detected yet.</p>
      ) : (
        <div className="alert-list">
          {chronic.map((c) => (
            <div key={c.id} className="alert-card" style={{borderLeftColor:'#FF00FF'}}>
              <div className="alert-info">
                <h4>♾ {c.fire_type} — Chronic Source</h4>
                <p>📍 Lat: {c.latitude?.toFixed(3)}, Lon: {c.longitude?.toFixed(3)}</p>
                <p>⚡ FRP: {c.frp} MW &nbsp;|&nbsp; 📅 {c.acq_date}</p>
                <p>🎯 Confidence: {c.confidence_score ? (c.confidence_score * 100).toFixed(0) : 0}%</p>
              </div>
              <span className="alert-badge badge-chronic">CHRONIC</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Alerts;