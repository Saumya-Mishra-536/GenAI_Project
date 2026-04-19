import React, { useState, useEffect, createContext, useContext } from 'react';
import { Routes, Route } from 'react-router-dom';
import AppShell from './components/AppShell';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Predict from './pages/Predict';
import BatchProcess from './pages/BatchProcess';
import AgentPlanner from './pages/AgentPlanner';
import { checkUploadStatus } from './api/client';

export const DataContext = createContext();

export const useDataContext = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useDataContext must be used within DataProvider');
  }
  return context;
};

function App() {
  const [dataUploaded, setDataUploaded] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(true);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const status = await checkUploadStatus();
        setDataUploaded(status.data_uploaded || status.has_processed_data);
      } catch (err) {
        console.error('Failed to check upload status:', err);
      } finally {
        setLoadingStatus(false);
      }
    };

    checkStatus();
  }, []);

  return (
    <DataContext.Provider value={{ dataUploaded, setDataUploaded, loadingStatus }}>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route element={<AppShell />}>
          <Route path="/overview" element={<Dashboard />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/batch" element={<BatchProcess />} />
          <Route path="/planner" element={<AgentPlanner />} />
        </Route>
      </Routes>
    </DataContext.Provider>
  );
}

export default App;
