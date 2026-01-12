import { useState, useEffect } from 'react';
import TaskInput from './TaskInput';
import AgentLog from './AgentLog';
import ResponseDisplay from './ResponseDisplay';
import MemoryViewer from './MemoryViewer';
import { api, connectWebSocket } from '../services/api';
import { Activity, Brain, MessageSquare } from 'lucide-react';

const Dashboard = () => {
  const [logs, setLogs] = useState([]);
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('task'); // 'task' or 'memory'
  const [ws, setWs] = useState(null);

  // WebSocket connection
  useEffect(() => {
    const websocket = connectWebSocket((data) => {
      // Add new log entry
      const newLog = {
        agent: data.agent || 'system',
        type: data.type || 'info',
        message: data.message || '',
        timestamp: new Date().toLocaleTimeString(),
      };
      setLogs((prev) => [...prev, newLog]);
    });

    setWs(websocket);

    // Cleanup on unmount
    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  const handleTaskSubmit = async (taskDescription) => {
    setIsLoading(true);
    setResponse(null);
    setLogs([]);

    // Add initial log
    setLogs([
      {
        agent: 'orchestrator',
        type: 'start',
        message: `Task received: ${taskDescription}`,
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);

    try {
      const result = await api.executeTask(taskDescription);
      setResponse(result);

      // Add completion log
      setLogs((prev) => [
        ...prev,
        {
          agent: 'orchestrator',
          type: 'complete',
          message: 'Task completed successfully!',
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } catch (error) {
      console.error('Task execution error:', error);
      setResponse({
        status: 'error',
        error: error.message || 'Failed to execute task',
      });

      // Add error log
      setLogs((prev) => [
        ...prev,
        {
          agent: 'orchestrator',
          type: 'error',
          message: `Error: ${error.message}`,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMemorySearch = async (query) => {
    try {
      const results = await api.searchMemory(query);
      return results.memories || [];
    } catch (error) {
      console.error('Memory search error:', error);
      return [];
    }
  };

  const handleMemoryClear = async () => {
    try {
      await api.clearMemory();
    } catch (error) {
      console.error('Clear memory error:', error);
      throw error;
    }
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <Activity size={32} />
          <h1>AI Agent Orchestration System</h1>
          <p>Multi-agent system for research, coding, and execution</p>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'task' ? 'active' : ''}`}
          onClick={() => setActiveTab('task')}
        >
          <MessageSquare size={20} />
          Task Execution
        </button>
        <button
          className={`tab-button ${activeTab === 'memory' ? 'active' : ''}`}
          onClick={() => setActiveTab('memory')}
        >
          <Brain size={20} />
          Memory Viewer
        </button>
      </div>

      {/* Main Content */}
      <div className="dashboard-content">
        {activeTab === 'task' ? (
          <>
            {/* Task Input Section */}
            <div className="section">
              <TaskInput onSubmit={handleTaskSubmit} isLoading={isLoading} />
            </div>

            {/* Two Column Layout */}
            <div className="two-column-layout">
              {/* Agent Log */}
              <div className="section">
                <AgentLog logs={logs} />
              </div>

              {/* Response Display */}
              <div className="section">
                <ResponseDisplay response={response} isLoading={isLoading} />
              </div>
            </div>
          </>
        ) : (
          <div className="section">
            <MemoryViewer onSearch={handleMemorySearch} onClear={handleMemoryClear} />
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>Built with React + FastAPI | Agent-Based AI System</p>
      </footer>
    </div>
  );
};

export default Dashboard;