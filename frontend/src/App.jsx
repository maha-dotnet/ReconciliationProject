import React, { useEffect, useState } from "react";

import ReconciliationTable from "./components/ReconciliationTable";
import {
  uploadCSV,
  reconcileRecords,
  getResults,
  getDashboard,
} from "./services/api";

import "./App.css";

function App() {
  const [systemAFile, setSystemAFile] = useState(null);
  const [systemBFile, setSystemBFile] = useState(null);

  const [results, setResults] = useState([]);
  const [dashboard, setDashboard] = useState({
    total: 0,
    matched: 0,
    mismatched: 0,
    missing: 0,
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    try {
      const data = await getDashboard();

      setDashboard({
        total: data.total ?? 0,
        matched: data.matched ?? 0,
        mismatched: data.mismatched ?? 0,
        missing: data.missing ?? 0,
      });
    } catch (err) {
      console.error("Dashboard error:", err);
    }
  };

  const loadResults = async () => {
    try {
      const data = await getResults();

      // Supports either a direct array or a paginated response.
      setResults(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      console.error("Results error:", err);
    }
  };

  useEffect(() => {
    loadResults();
    loadDashboard();
  }, []);

  const handleUpload = async (system, file) => {
    if (!file) {
      setError(`Please select a ${system.toUpperCase()} CSV file.`);
      return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
      setError("Please select a valid CSV file.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const response = await uploadCSV(system, file);

      setMessage(
        response.message || `${system.toUpperCase()} file uploaded successfully.`
      );

      if (system === "system_a") {
        setSystemAFile(null);
      } else {
        setSystemBFile(null);
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
          err.response?.data?.message ||
          "File upload failed. Check the Django backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReconcile = async () => {
    setLoading(true);
    setError("");
    setMessage("");

    try {
      const response = await reconcileRecords();

      setMessage(
        response.message || "Reconciliation completed successfully."
      );

      await loadResults();
      await loadDashboard();
    } catch (err) {
      setError(
        err.response?.data?.error ||
          err.response?.data?.message ||
          "Reconciliation failed. Please check the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    setError("");

    try {
      await loadResults();
      await loadDashboard();
      setMessage("Data refreshed successfully.");
    } catch {
      setError("Unable to refresh data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Reconciliation Dashboard</h1>
        <p>Compare financial transactions between System A and System B.</p>
      </header>

      <main className="main-content">
        <section className="dashboard">
          <div className="dashboard-card">
            <h3>Total Records</h3>
            <p>{dashboard.total}</p>
          </div>

          <div className="dashboard-card matched-card">
            <h3>Matched</h3>
            <p>{dashboard.matched}</p>
          </div>

          <div className="dashboard-card mismatch-card">
            <h3>Mismatched</h3>
            <p>{dashboard.mismatched}</p>
          </div>

          <div className="dashboard-card missing-card">
            <h3>Missing</h3>
            <p>{dashboard.missing}</p>
          </div>
        </section>

        <section className="upload-section">
          <h2>Upload CSV Files</h2>

          <div className="upload-grid">
            <div className="upload-card">
              <h3>System A</h3>

              <input
                type="file"
                accept=".csv"
                onChange={(e) => setSystemAFile(e.target.files?.[0] || null)}
              />

              <button
                disabled={loading || !systemAFile}
                onClick={() => handleUpload("system_a", systemAFile)}
              >
                Upload System A
              </button>
            </div>

            <div className="upload-card">
              <h3>System B</h3>

              <input
                type="file"
                accept=".csv"
                onChange={(e) => setSystemBFile(e.target.files?.[0] || null)}
              />

              <button
                disabled={loading || !systemBFile}
                onClick={() => handleUpload("system_b", systemBFile)}
              >
                Upload System B
              </button>
            </div>
          </div>
        </section>

        <section className="action-section">
          <button
            className="reconcile-button"
            disabled={loading}
            onClick={handleReconcile}
          >
            Reconcile Transactions
          </button>

          <button
            className="refresh-button"
            disabled={loading}
            onClick={handleRefresh}
          >
            Refresh Results
          </button>
        </section>

        {loading && <p className="info-message">Please wait...</p>}
        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}

        <section className="results-section">
          <h2>Reconciliation Results</h2>
          <ReconciliationTable results={results} />
        </section>
      </main>
    </div>
  );
}

export default App;