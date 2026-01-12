import { useState, useEffect } from 'react';
import { Brain, Search, Trash2, Calendar, RefreshCw } from 'lucide-react';

const MemoryViewer = ({ onSearch, onClear }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [memories, setMemories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSearchMode, setIsSearchMode] = useState(false);

  // Load all memories on component mount
  useEffect(() => {
    loadAllMemories();
  }, []);

  const loadAllMemories = async () => {
    setIsLoading(true);
    setIsSearchMode(false);
    try {
      const response = await fetch('http://localhost:8000/api/memory/history?limit=50');
      const data = await response.json();
      setMemories(data.history || []);
    } catch (error) {
      console.error('Failed to load memories:', error);
      setMemories([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      loadAllMemories();
      return;
    }

    setIsLoading(true);
    setIsSearchMode(true);
    try {
      const results = await onSearch(searchQuery);
      setMemories(results);
    } catch (error) {
      console.error('Memory search error:', error);
      setMemories([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Are you sure you want to clear all memories? This cannot be undone.')) {
      try {
        await onClear();
        setMemories([]);
        setSearchQuery('');
        alert('Memory cleared successfully!');
      } catch (error) {
        console.error('Clear memory error:', error);
        alert('Failed to clear memory');
      }
    }
  };

  const handleRefresh = () => {
    setSearchQuery('');
    loadAllMemories();
  };

  return (
    <div className="memory-viewer-container">
      <div className="memory-header">
        <Brain size={24} />
        <h3>Memory Viewer</h3>
        <div className="memory-actions">
          <button onClick={handleRefresh} className="refresh-button" title="Refresh">
            <RefreshCw size={18} />
          </button>
          <button onClick={handleClear} className="clear-button" title="Clear All Memory">
            <Trash2 size={18} />
            Clear All
          </button>
        </div>
      </div>

      <form onSubmit={handleSearch} className="memory-search-form">
        <div className="search-input-group">
          <Search size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search memories... (e.g., 'python code', 'AI research')"
            className="memory-search-input"
          />
          <button type="submit" className="search-button" disabled={isLoading}>
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {isSearchMode && (
        <div className="search-mode-indicator">
          <span>Showing search results for: "{searchQuery}"</span>
          <button onClick={handleRefresh} className="show-all-button">
            Show All
          </button>
        </div>
      )}

      <div className="memory-results">
        {isLoading ? (
          <div className="loading-memories">
            <div className="loading-spinner large"></div>
            <p>Loading memories...</p>
          </div>
        ) : memories.length === 0 ? (
          <div className="empty-memories">
            <Brain size={48} className="empty-icon" />
            <p>
              {isSearchMode 
                ? 'No memories found for your search. Try different keywords.'
                : 'No memories yet. Complete some tasks to build memory.'}
            </p>
          </div>
        ) : (
          <div className="memory-list">
            <div className="memory-count-badge">
              {memories.length} {memories.length === 1 ? 'memory' : 'memories'} found
            </div>
            {memories.map((memory, index) => (
              <div key={index} className="memory-item">
                <div className="memory-meta">
                  <span className="memory-type">
                    {memory.agent_name || memory.type || 'conversation'}
                  </span>
                  <span className="memory-date">
                    <Calendar size={14} />
                    {memory.timestamp || memory.created_at || 'Unknown date'}
                  </span>
                </div>
                <div className="memory-task">
                  <strong>Task:</strong> {memory.task || memory.query || 'N/A'}
                </div>
                <div className="memory-content">
                  {memory.result || memory.content || memory.message}
                </div>
                {memory.relevance_score && (
                  <div className="memory-score">
                    Relevance: {(memory.relevance_score * 100).toFixed(1)}%
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MemoryViewer;