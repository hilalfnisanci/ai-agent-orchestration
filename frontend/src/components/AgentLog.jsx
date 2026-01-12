import { useEffect, useRef } from 'react';
import { Activity, Search, Code, Play, Brain } from 'lucide-react';

const AgentLog = ({ logs }) => {
  const logContainerRef = useRef(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const getAgentIcon = (agentType) => {
    switch (agentType) {
      case 'search':
        return <Search size={16} />;
      case 'coding':
        return <Code size={16} />;
      case 'execution':
        return <Play size={16} />;
      case 'orchestrator':
        return <Brain size={16} />;
      default:
        return <Activity size={16} />;
    }
  };

  const getLogTypeClass = (type) => {
    switch (type) {
      case 'start':
        return 'log-start';
      case 'thinking':
        return 'log-thinking';
      case 'action':
        return 'log-action';
      case 'complete':
        return 'log-complete';
      case 'error':
        return 'log-error';
      default:
        return 'log-info';
    }
  };

  return (
    <div className="agent-log-container">
      <div className="agent-log-header">
        <Activity size={20} />
        <h3>Agent Activity Log</h3>
        <span className="log-count">{logs.length} events</span>
      </div>
      <div className="agent-log-content" ref={logContainerRef}>
        {logs.length === 0 ? (
          <div className="empty-log">
            <Activity size={48} className="empty-icon" />
            <p>No activity yet. Submit a task to see agents in action!</p>
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={`log-entry ${getLogTypeClass(log.type)}`}>
              <div className="log-icon">
                {getAgentIcon(log.agent)}
              </div>
              <div className="log-details">
                <div className="log-meta">
                  <span className="log-agent">{log.agent}</span>
                  <span className="log-time">{log.timestamp}</span>
                </div>
                <div className="log-message">{log.message}</div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AgentLog;