import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import api from './services/api';
import './App.css';

function App() {
  const [isHealthy, setIsHealthy] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await api.health();
        setIsHealthy(true);
      } catch (error) {
        console.error('Backend health check failed:', error);
        setIsHealthy(false);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
  }, []);

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1>KYNEĒ Console</h1>
            <p>Autonomous Penetration Testing Platform</p>
          </div>
          <nav className="nav">
            <Link to="/">Dashboard</Link>
            <Link to="/agents">Agents</Link>
            <Link to="/findings">Findings</Link>
            <Link to="/engagements">Engagements</Link>
          </nav>
        </header>

        <main className="app-main">
          {loading ? (
            <div className="loading">Loading...</div>
          ) : !isHealthy ? (
            <div className="error">
              <h2>⚠️ Backend Connection Failed</h2>
              <p>Unable to connect to the KYNEĒ console backend.</p>
              <p>Please ensure the backend is running on http://localhost:8000</p>
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/agents" element={<AgentsPage />} />
              <Route path="/findings" element={<FindingsPage />} />
              <Route path="/engagements" element={<EngagementsPage />} />
            </Routes>
          )}
        </main>
      </div>
    </Router>
  );
}

// Placeholder pages
function Dashboard() {
  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome to KYNEĒ Console</p>
    </div>
  );
}

function AgentsPage() {
  return (
    <div>
      <h2>Agents</h2>
      <p>No agents enrolled yet</p>
    </div>
  );
}

function FindingsPage() {
  return (
    <div>
      <h2>Findings</h2>
      <p>No findings yet</p>
    </div>
  );
}

function EngagementsPage() {
  return (
    <div>
      <h2>Engagements</h2>
      <p>No engagements yet</p>
    </div>
  );
}

export default App;
