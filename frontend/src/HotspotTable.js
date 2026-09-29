import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FIRE_CLASS = {
  'Industrial Fire': 'fire-industrial',
  'Wildfire': 'fire-wildfire',
  'Agricultural Burning': 'fire-agricultural',
  'Gas Flare': 'fire-gasflare',
};

function HotspotTable() {
  const [hotspots, setHotspots] = useState([]);
  const [filter, setFilter] = useState('All');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchHotspots = async () => {
    try {
     const res = await axios.get('https://firewatch-india-production.up.railway.app/api/hotspots');
      setHotspots(res.data.hotspots);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchHotspots();
  }, []);

  const filtered = hotspots.filter(h => {
    const matchType = filter === 'All' || h.fire_type === filter;
    const matchSearch = search === '' ||
      h.fire_type?.toLowerCase().includes(search.toLowerCase()) ||
      h.satellite?.toLowerCase().includes(search.toLowerCase()) ||
      h.acq_date?.includes(search);
    return matchType && matchSearch;
  });

  if (loading) return <p style={{color:'#aaa', padding:'20px'}}>Loading hotspots...</p>;

  return (
    <div>
      <h2 className="page-title">All Detected Hotspots</h2>
      <div className="controls" style={{marginBottom:'20px'}}>
        <select onChange={(e) => setFilter(e.target.value)}>
          <option value="All">All Types</option>
          <option value="Industrial Fire">Industrial Fire</option>
          <option value="Wildfire">Wildfire</option>
          <option value="Agricultural Burning">Agricultural Burning</option>
          <option value="Gas Flare">Gas Flare</option>
        </select>
        <input
          type="text"
          placeholder="Search by date, satellite..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: '10px',
            borderRadius: '8px',
            background: '#1a1a1a',
            color: 'white',
            border: '1px solid #444',
            fontSize: '14px',
            width: '250px'
          }}
        />
        <span style={{color:'#aaa', fontSize:'13px'}}>
          {filtered.length} records
        </span>
      </div>
      <div style={{overflowX:'auto'}}>
        <table className="hotspot-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Fire Type</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>FRP (MW)</th>
              <th>Confidence</th>
              <th>Satellite</th>
              <th>Date</th>
              <th>Chronic</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((h, index) => (
              <tr key={h.id}>
                <td>{index + 1}</td>
                <td>
                  <span className={`fire-badge ${FIRE_CLASS[h.fire_type]}`}>
                    {h.fire_type}
                  </span>
                </td>
                <td>{h.latitude?.toFixed(3)}</td>
                <td>{h.longitude?.toFixed(3)}</td>
                <td>{h.frp || 'N/A'}</td>
                <td>{h.confidence_score ? (h.confidence_score * 100).toFixed(0) + '%' : 'N/A'}</td>
                <td>
                      {h.satellite === 'N' ? 'Suomi NPP' : 
                      h.satellite === 'A' ? 'Terra' : 
                      h.satellite === 'T' ? 'Aqua' : 
                      h.satellite === '1' ? 'NOAA-20' : 
                      h.satellite || 'N/A'}
                </td>
                <td>{h.acq_date}</td>
                <td>
                  <span style={{color: h.is_chronic === 'yes' ? '#FF44FF' : '#44FF44'}}>
                    {h.is_chronic === 'yes' ? 'Yes' : 'No'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HotspotTable;