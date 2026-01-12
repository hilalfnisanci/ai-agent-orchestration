import { CheckCircle, XCircle, Clock, Code, ExternalLink } from 'lucide-react';

const ResponseDisplay = ({ response, isLoading }) => {
  if (isLoading) {
    return (
      <div className="response-container">
        <div className="response-loading">
          <div className="loading-spinner large"></div>
          <p>Agents are working on your task...</p>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="response-container">
        <div className="response-empty">
          <Clock size={48} className="empty-icon" />
          <p>No results yet. Submit a task to see responses!</p>
        </div>
      </div>
    );
  }

  // Extract data from orchestration response
  const orchestration = response.orchestration || {};
  const agentResponse = orchestration.agent_response || {};
  const metadata = agentResponse.metadata || {};
  const results = metadata.results || [];

  return (
    <div className="response-container">
      <div className="response-header">
        {response.status === 'success' ? (
          <CheckCircle size={24} className="status-success" />
        ) : (
          <XCircle size={24} className="status-error" />
        )}
        <h3>Task Result</h3>
      </div>

      <div className="response-content">
        {/* Main Result */}
        <div className="response-section">
          <h4>Result</h4>
          <div className="response-text">
            {agentResponse.result || response.message || 'No result available'}
          </div>
        </div>

        {/* Task Info */}
        {orchestration.task && (
          <div className="response-section">
            <h4>Task</h4>
            <div className="response-text">
              {orchestration.task}
            </div>
          </div>
        )}

        {/* Search Results (if any) */}
        {results.length > 0 && (
          <div className="response-section">
            <h4>Search Results ({results.length})</h4>
            <ul className="sources-list">
              {results.map((result, index) => (
                <li key={index}>
                  <ExternalLink size={14} />
                  <div>
                    <a href={result.url} target="_blank" rel="noopener noreferrer">
                      {result.title}
                    </a>
                    {result.snippet && (
                      <p className="result-snippet">{result.snippet}</p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Code Output (if any) */}
        {agentResponse.code && (
          <div className="response-section">
            <h4>
              <Code size={18} />
              Generated Code
            </h4>
            <pre className="code-block">
              <code>{agentResponse.code}</code>
            </pre>
          </div>
        )}

        {/* Execution Output (if any) */}
        {agentResponse.output && (
          <div className="response-section">
            <h4>Execution Output</h4>
            <pre className="output-block">
              {agentResponse.output}
            </pre>
          </div>
        )}

        {/* Error (if any) */}
        {agentResponse.error && (
          <div className="response-section error-section">
            <h4>Error</h4>
            <div className="error-text">
              {agentResponse.error}
            </div>
          </div>
        )}

        {/* Metadata */}
        <div className="response-metadata">
          <span>Agent: {agentResponse.agent_name || orchestration.agent_type || 'Unknown'}</span>
          <span>Status: {agentResponse.status || response.status}</span>
          {metadata.results_count && (
            <span>Results: {metadata.results_count}</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResponseDisplay;