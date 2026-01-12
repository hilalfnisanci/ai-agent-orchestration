import { useState } from 'react';
import { Brain, Search, Trash2, Calendar } from 'lucide-react';

const MemoryViewer = ({ onSearch, onClear }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [memories, setMemories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    try {
      const results = await onSearch(searchQuery);
      setMemories(results);
    } catch (error) {
      console.error('Memory search error:', error);
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

  return (
    <div className="memory-viewer-container">
      <div className="memory-header">
        <Brain size={24} />
        <h3>Memory Viewer</h3>
        <button onClick={handleClear} className="clear-button" title="Clear All Memory">
          <Trash2 size={18} />
          Clear All
        </button>
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

      <div className="memory-results">
        {memories.length === 0 ? (
          <div className="empty-memories">
            <Brain size={48} className="empty-icon" />
            <p>No memories found. Try searching for past conversations or tasks.</p>
          </div>
        ) : (
          <div className="memory-list">
            {memories.map((memory, index) => (
              <div key={index} className="memory-item">
                <div className="memory-meta">
                  <span className="memory-type">{memory.type || 'conversation'}</span>
                  <span className="memory-date">
                    <Calendar size={14} />
                    {memory.timestamp || 'Unknown date'}
                  </span>
                </div>
                <div className="memory-content">
                  {memory.content || memory.message}
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