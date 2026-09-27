import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, LayersControl } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

const { BaseLayer } = LayersControl;

const FIRE_COLORS = {
  'Industrial Fire': '#FF0000',
  'Wildfire': '#FF6600',
  'Agricultural Burning': '#FFD700',
  'Gas Flare': '#FF00FF',
};

function Dashboard() {
  const [hotspots, setHotspots] = useState([]);
  const [allHotspots, setAllHotspots] = useState([]);
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('All');
  const [alertBanner, setAlertBanner] = useState('');
  const [selectedDate, setSelectedDate] = useState('All');
  const [availableDates, setAvailableDates] = useState([]);

  const updateSummary = (data) => {
    setSummary({
      industrial_fire: data.filter(h => h.fire_type === 'Industrial Fire').length,
      wildfire: data.filter(h => h.fire_type === 'Wildfire').length,
      agricultural_burning: data.filter(h => h.fire_type === 'Agricultural Burning').length,
      gas_flare: data.filter(h => h.fire_type === 'Gas Flare').length,
      chronic_sources: data.filter(h => h.is_chronic === 'yes').length,
      total_hotspots: data.length
    });
  };

  const fetchHotspots = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/hotspots');
      const data = res.data.hotspots;
      setAllHotspots(data);

      const dates = [...new Set(data.map(h => h.acq_date))].sort().reverse();
      setAvailableDates(dates);

      if (dates.length > 0) {
        const latest = data.filter(h => h.acq_date === dates[0]);
        setSelectedDate(dates[0]);
        setHotspots(latest);
        updateSummary(latest);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchFromFIRMS = async () => {
    setLoading(true);
    try {
      await axios.post('http://127.0.0.1:8000/api/hotspots/fetch?days=5');
      await fetchHotspots();

      const alertRes = await axios.get('http://127.0.0.1:8000/api/alerts');
      const alerts = alertRes.data.alerts;

      if (alerts.length > 0) {
        if (Notification.permission === 'granted') {
          new Notification('🔥 FireWatch India Alert!', {
            body: `${alerts.length} high priority fires detected! ${alerts[0].fire_type} near ${alerts[0].latitude.toFixed(2)}, ${alerts[0].longitude.toFixed(2)}`,
            icon: '/favicon.ico'
          });
        }
        setAlertBanner(`🚨 ${alerts.length} HIGH PRIORITY ALERTS — ${alerts[0].fire_type} detected!`);
      } else {
        setAlertBanner('✅ No high priority alerts detected.');
        setTimeout(() => setAlertBanner(''), 3000);
      }

    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleDateChange = (date) => {
    setSelectedDate(date);
    setFilter('All');
    let filtered;
    if (date === 'All') {
      filtered = allHotspots;
    } else {
      filtered = allHotspots.filter(h => h.acq_date === date);
    }
    setHotspots(filtered);
    updateSummary(filtered);
  };

  useEffect(() => {
    fetchHotspots();
    if (Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  const filteredHotspots = filter === 'All'
    ? hotspots
    : hotspots.filter(h => h.fire_type === filter);

  return (
    <div>
      <h2 className="page-title">🛰 Live Fire Map — India</h2>

      {alertBanner && (
        <div style={{
          background: alertBanner.startsWith('✅') ? '#1f3a1f' : '#3d1f1f',
          border: `1px solid ${alertBanner.startsWith('✅') ? '#3fb950' : '#f85149'}`,
          borderLeft: `4px solid ${alertBanner.startsWith('✅') ? '#3fb950' : '#f85149'}`,
          borderRadius: '8px',
          padding: '14px 20px',
          marginBottom: '20px',
          color: alertBanner.startsWith('✅') ? '#3fb950' : '#f85149',
          fontWeight: 'bold',
          fontSize: '15px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          {alertBanner}
          <button onClick={() => setAlertBanner('')} style={{background:'none', border:'none', color:'inherit', cursor:'pointer', fontSize:'18px'}}>✕</button>
        </div>
      )}

      <div className="summary">
        <div className="card red"><h3>{summary.industrial_fire || 0}</h3><p>Industrial Fires</p></div>
        <div className="card orange"><h3>{summary.wildfire || 0}</h3><p>Wildfires</p></div>
        <div className="card yellow"><h3>{summary.agricultural_burning || 0}</h3><p>Agricultural Burning</p></div>
        <div className="card purple"><h3>{summary.gas_flare || 0}</h3><p>Gas Flares</p></div>
        <div className="card gray"><h3>{summary.chronic_sources || 0}</h3><p>Chronic Sources</p></div>
      </div>

      <div className="controls">
        <button className="btn btn-primary" onClick={fetchFromFIRMS} disabled={loading}>
          {loading ? '⏳ Fetching...' : '🛰 Fetch from NASA FIRMS'}
        </button>
        <select onChange={(e) => handleDateChange(e.target.value)} value={selectedDate}>
          <option value="All">All Dates</option>
          {availableDates.map(date => (
            <option key={date} value={date}>{date}</option>
          ))}
        </select>
        <select onChange={(e) => setFilter(e.target.value)} value={filter}>
          <option value="All">All Types</option>
          <option value="Industrial Fire">Industrial Fire</option>
          <option value="Wildfire">Wildfire</option>
          <option value="Agricultural Burning">Agricultural Burning</option>
          <option value="Gas Flare">Gas Flare</option>
        </select>
        <span style={{color:'#aaa', fontSize:'13px'}}>{filteredHotspots.length} hotspots showing</span>
      </div>

      <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{height:'520px', width:'100%', borderRadius:'10px'}}>
        <LayersControl position="topright">
          <BaseLayer checked name="🗺 Street View">
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="OpenStreetMap"
            />
          </BaseLayer>
          <BaseLayer name="🛰 Satellite View">
            <TileLayer
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
              attribution="Esri World Imagery"
            />
          </BaseLayer>
          <BaseLayer name="🌙 Dark View">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution="CartoDB"
            />
          </BaseLayer>
        </LayersControl>

        {filteredHotspots.map((h) => (
          <CircleMarker
            key={h.id}
            center={[h.latitude, h.longitude]}
            radius={7}
            fillColor={FIRE_COLORS[h.fire_type] || '#FF0000'}
            color="#000"
            weight={1}
            fillOpacity={0.85}
          >
            <Popup>
              <div style={{minWidth:'180px'}}>
                <b style={{fontSize:'14px'}}>🔥 {h.fire_type}</b>
                <hr style={{margin:'6px 0', borderColor:'#ddd'}}/>
                <p>📍 {h.latitude.toFixed(3)}, {h.longitude.toFixed(3)}</p>
                <p>⚡ FRP: <b>{h.frp} MW</b></p>
                <p>🎯 Confidence: <b>{(h.confidence_score * 100).toFixed(0)}%</b></p>
                <p>🛰 Satellite: {h.satellite === 'N' ? 'Suomi NPP (VIIRS)' : h.satellite === 'A' ? 'Terra (MODIS)' : h.satellite === 'T' ? 'Aqua (MODIS)' : h.satellite === '1' ? 'NOAA-20' : h.satellite}</p>
                <p>📅 Date: {h.acq_date}</p>
                <p>🏭 Industry Nearby: {h.industrial_nearby ? 'Yes' : 'No'}</p>
                <p>⚠️ Chronic: <b style={{color: h.is_chronic === 'yes' ? 'red' : 'green'}}>{h.is_chronic}</b></p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      <div className="legend" style={{marginTop:'15px'}}>
        <div className="legend-item"><span style={{background:'#FF0000'}}></span>Industrial Fire</div>
        <div className="legend-item"><span style={{background:'#FF6600'}}></span>Wildfire</div>
        <div className="legend-item"><span style={{background:'#FFD700'}}></span>Agricultural Burning</div>
        <div className="legend-item"><span style={{background:'#FF00FF'}}></span>Gas Flare</div>
      </div>
    </div>
  );
}

export default Dashboard;