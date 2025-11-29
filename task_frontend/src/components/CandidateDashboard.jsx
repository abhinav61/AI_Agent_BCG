import { useState } from 'react';
import { FaSearch, FaUsers, FaCheckCircle, FaClock, FaExclamationTriangle, FaEye, FaInbox } from 'react-icons/fa';
import './CandidateDashboard.css';

const CandidateDashboard = ({ candidates, onCandidateSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const getStatusBadgeClass = (status) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'status-badge status-completed';
      case 'processing':
        return 'status-badge status-processing';
      case 'pending':
        return 'status-badge status-pending';
      case 'verification failed':
      case 'failed':
        return 'status-badge status-failed';
      default:
        return 'status-badge';
    }
  };

  const filteredCandidates = candidates.filter((candidate) => {
    const matchesSearch = 
      candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.company.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = 
      filterStatus === 'all' || 
      candidate.extractionStatus.toLowerCase() === filterStatus.toLowerCase();
    
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Candidate Dashboard</h1>
        <p className="dashboard-subtitle">
          Manage and track candidate resume extractions
        </p>
      </div>

      <div className="dashboard-controls">
        <div className="search-bar">
         
          <input
            type="text"
            placeholder="Search by name, email, or company..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-box">
          <label htmlFor="status-filter">Filter by Status:</label>
          <select
            id="status-filter"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="processing">Processing</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
        </div>
      </div>

      <div className="stats-container">
        <div className="stat-card">
          <FaUsers className="stat-icon" size={24} />
          <div className="stat-value">{candidates.length}</div>
          <div className="stat-label">Total Candidates</div>
        </div>
        <div className="stat-card">
          <FaCheckCircle className="stat-icon" size={24} />
          <div className="stat-value">
            {candidates.filter(c => c.extractionStatus === 'Completed').length}
          </div>
          <div className="stat-label">Completed</div>
        </div>
        <div className="stat-card">
          <FaClock className="stat-icon" size={24} />
          <div className="stat-value">
            {candidates.filter(c => c.extractionStatus === 'Processing').length}
          </div>
          <div className="stat-label">Processing</div>
        </div>
        <div className="stat-card">
          <FaExclamationTriangle className="stat-icon" size={24} />
          <div className="stat-value">
            {candidates.filter(c => c.extractionStatus === 'Pending').length}
          </div>
          <div className="stat-label">Pending</div>
        </div>
      </div>

      <div className="table-container">
        <table className="candidates-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Company</th>
              <th>Extraction Status</th>
              <th>Upload Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredCandidates.length === 0 ? (
              <tr>
                <td colSpan="6" className="empty-state">
                  <FaInbox className="empty-icon" size={48} />
                  <p>No candidates found</p>
                </td>
              </tr>
            ) : (
              filteredCandidates.map((candidate) => (
                <tr key={candidate.id} className="table-row">
                  <td className="candidate-name">
                    <div className="avatar">{candidate.name.charAt(0).toUpperCase()}</div>
                    {candidate.name}
                  </td>
                  <td className="candidate-email">{candidate.email}</td>
                  <td>{candidate.company}</td>
                  <td>
                    <span className={getStatusBadgeClass(candidate.extractionStatus)}>
                      {candidate.extractionStatus}
                    </span>
                  </td>
                  <td>{new Date(candidate.uploadDate).toLocaleDateString()}</td>
                  <td>
                    <button
                      className="view-btn"
                      onClick={() => onCandidateSelect(candidate)}
                    >
                      <FaEye /> View Details
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CandidateDashboard;
