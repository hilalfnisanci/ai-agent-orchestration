import { useState } from 'react';
import { Send } from 'lucide-react';

const TaskInput = ({ onSubmit, isLoading }) => {
  const [task, setTask] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (task.trim()) {
      onSubmit(task);
      setTask('');
    }
  };

  return (
    <div className="task-input-container">
      <form onSubmit={handleSubmit} className="task-form">
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Enter your task here... (e.g., 'Search for latest AI trends' or 'Write a Python function to calculate fibonacci')"
          className="task-textarea"
          rows="4"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="submit-button"
          disabled={isLoading || !task.trim()}
        >
          {isLoading ? (
            <>
              <span className="loading-spinner"></span>
              Processing...
            </>
          ) : (
            <>
              <Send size={20} />
              Execute Task
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default TaskInput;