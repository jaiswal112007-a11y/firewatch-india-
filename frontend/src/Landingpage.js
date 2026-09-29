import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function LandingPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    total: 0,
    industrial: 0,
    wildfire: 0,
    agricultural: 0,
  });
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    axios.get('https://firewatch-india-production.up.railway.app/api/alerts/summary')
      .then(res => {
        setStats({
          total: res.data.total_hotspots,
          industrial: res.data.industrial_fire,
          wildfire: res.data.wildfire,
          agricultural: res.data.agricultural_burning,
        });
      })
      .catch(err => console.error(err));

    // Fire particles
    const p = Array.from({length: 30}, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 3 + Math.random() * 4,
      size: 6 + Math.random() * 14,
    }));
    setParticles(p);
  }, []);

  return (
    <div style={styles.container}>

      {/* Animated fire particles */}
      {particles.map(p => (
        <div
          key={p.id}
          style={{
            position: 'absolute',
            left: `${p.left}%`,
            bottom: '-20px',
            width: `${p.size}px`,
            height: `${p.size}px`,
            borderRadius: '50% 50% 50% 0',
            background: `radial-gradient(circle, #FFD700, #FF4500, #FF0000)`,
            opacity: 0.7,
            animation: `rise ${p.duration}s ${p.delay}s infinite ease-in`,
            zIndex: 1,
          }}
        />
      ))}

      {/* CSS Animation */}
      <style>{`
        @keyframes rise {
          0% { transform: translateY(0) scale(1); opacity: 0.7; }
          100% { transform: translateY(-100vh) scale(0); opacity: 0; }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        @keyframes glow {
          0%, 100% { text-shadow: 0 0 20px #FF4500, 0 0 40px #FF4500; }
          50% { text-shadow: 0 0 40px #FF4500, 0 0 80px #FF0000, 0 0 120px #FF0000; }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>


      {/* Hero */}
      <div style={styles.hero}>

        {/* Fire emoji animated */}
        <div style={{fontSize: '80px', animation: 'pulse 2s infinite', marginBottom: '20px'}}>
          🔥
        </div>

        {/* Main title */}
        <h1 style={styles.title}>FireWatch India</h1>

        {/* One line pitch */}
        <p style={styles.pitch}>
          NASA FIRMS detects fires.<br/>
          <span style={{color: '#FF4500', fontWeight: 'bold'}}>We classify them.</span>
        </p>

        {/* Subtitle */}
        <p style={styles.subtitle}>
          AI-Based Detection and Classification of Industrial Fires<br/>
          using NASA FIRMS · OSM · Satellite Data
        </p>

        {/* Live stats */}
        <div style={styles.statsRow}>
          <div style={styles.statItem}>
            <span style={{color: '#f85149', fontSize: '28px', fontWeight: 'bold'}}>{stats.total}</span>
            <span style={styles.statLabel}>Hotspots Classified</span>
          </div>
          <div style={styles.statDivider}/>
          <div style={styles.statItem}>
            <span style={{color: '#f85149', fontSize: '28px', fontWeight: 'bold'}}>{stats.industrial}</span>
            <span style={styles.statLabel}>Industrial Fires</span>
          </div>
          <div style={styles.statDivider}/>
          <div style={styles.statItem}>
            <span style={{color: '#58a6ff', fontSize: '28px', fontWeight: 'bold'}}>97%</span>
            <span style={styles.statLabel}>Model Accuracy</span>
          </div>
          <div style={styles.statDivider}/>
          <div style={styles.statItem}>
            <span style={{color: '#58a6ff', fontSize: '28px', fontWeight: 'bold'}}>375m</span>
            <span style={styles.statLabel}>VIIRS Resolution</span>
          </div>
        </div>

        {/* CTA Button */}
        <button
          style={styles.ctaButton}
          onClick={() => navigate('/dashboard')}
          onMouseEnter={e => {
            e.target.style.background = '#FF4500';
            e.target.style.transform = 'scale(1.05)';
          }}
          onMouseLeave={e => {
            e.target.style.background = 'transparent';
            e.target.style.transform = 'scale(1)';
          }}
        >
          🚀 Launch Dashboard
        </button>

        {/* Real incidents */}
        <div style={styles.incidents}>
          <div style={styles.incidentItem}>
            <span style={{color: '#f85149'}}>🏭</span>
            <span>Vizag Gas Leak 2020 — 11 dead</span>
          </div>
          <div style={styles.incidentItem}>
            <span style={{color: '#f85149'}}>🔥</span>
            <span>Baghjan Oil Fire 2020 — 6 months</span>
          </div>
          <div style={styles.incidentItem}>
            <span style={{color: '#f85149'}}>⛏</span>
            <span>Jharia Coal Fire — Since 1916</span>
          </div>
        </div>

      </div>

      {/* Footer */}
      <div style={styles.footer}>
        <p>Team GenSpark | SIH 2026 | PS 26162 | NTRO — Disaster Management</p>
        <p style={{color: '#484f58', marginTop: '4px', fontSize: '11px'}}>
          Powered by NASA FIRMS · OpenStreetMap · XGBoost · FastAPI · React · Leaflet
        </p>
      </div>

    </div>
  );
}

const styles = {
  container: {
    background: 'radial-gradient(ellipse at center, #1a0a00 0%, #0d0000 50%, #000000 100%)',
    minHeight: '100vh',
    color: '#e6edf3',
    fontFamily: 'Segoe UI, sans-serif',
    position: 'relative',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  topBar: {
    display: 'flex',
    gap: '10px',
    padding: '14px 30px',
    width: '100%',
    justifyContent: 'center',
    borderBottom: '1px solid #2a0a00',
    zIndex: 10,
    flexWrap: 'wrap',
  },
  topTag: {
    padding: '4px 14px',
    background: '#1a0500',
    border: '1px solid #FF4500',
    borderRadius: '20px',
    fontSize: '12px',
    color: '#FF6600',
  },
  hero: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    textAlign: 'center',
    padding: '40px 20px',
    zIndex: 10,
    animation: 'fadeIn 1s ease',
  },
  title: {
    fontSize: '64px',
    fontWeight: '900',
    color: '#ffffff',
    margin: '0 0 16px',
    animation: 'glow 3s infinite',
    letterSpacing: '2px',
  },
  pitch: {
    fontSize: '24px',
    color: '#c9d1d9',
    margin: '0 0 16px',
    lineHeight: '1.6',
  },
  subtitle: {
    fontSize: '15px',
    color: '#8b949e',
    margin: '0 0 36px',
    lineHeight: '1.8',
  },
  statsRow: {
    display: 'flex',
    gap: '0',
    background: 'rgba(255,69,0,0.08)',
    border: '1px solid rgba(255,69,0,0.3)',
    borderRadius: '12px',
    padding: '20px 30px',
    marginBottom: '36px',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  statItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '0 24px',
  },
  statLabel: {
    fontSize: '11px',
    color: '#8b949e',
    marginTop: '4px',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  statDivider: {
    width: '1px',
    background: 'rgba(255,69,0,0.3)',
    margin: '0 4px',
  },
  ctaButton: {
    padding: '16px 48px',
    background: 'transparent',
    color: '#FF4500',
    border: '2px solid #FF4500',
    borderRadius: '8px',
    fontSize: '18px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s',
    marginBottom: '40px',
    letterSpacing: '1px',
  },
  incidents: {
    display: 'flex',
    gap: '24px',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  incidentItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '13px',
    color: '#8b949e',
    padding: '8px 16px',
    background: 'rgba(248,81,73,0.08)',
    border: '1px solid rgba(248,81,73,0.2)',
    borderRadius: '20px',
  },
  footer: {
    textAlign: 'center',
    padding: '20px',
    borderTop: '1px solid #1a0500',
    color: '#8b949e',
    fontSize: '12px',
    zIndex: 10,
    width: '100%',
  },
};

export default LandingPage;