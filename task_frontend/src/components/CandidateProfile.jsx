import { useState } from 'react';
import { FaUser, FaEnvelope, FaMapMarkerAlt, FaBriefcase, FaGraduationCap, FaPaperPlane, FaEye, FaEyeSlash, FaArrowLeft } from 'react-icons/fa';
import DocumentSection from './DocumentSection';
import './CandidateProfile.css';

const CandidateProfile = ({ candidate, onBack, onRequestDocuments }) => {
  const [showDocuments, setShowDocuments] = useState(false);
  const [isRequesting, setIsRequesting] = useState(false);

  const handleRequestDocuments = async () => {
    setIsRequesting(true);
    try {
      const response = await fetch(`https://ai-agent-bcg.onrender.com/api/candidates/${candidate.id}/request-documents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Document request sent successfully to ${candidate.email}!\n\nAI Generated Message:\n${result.email_body.substring(0, 150)}...`);
        if (onRequestDocuments) {
          await onRequestDocuments(candidate.id);
        }
      } else {
        const error = await response.json();
        alert(`Failed to send document request: ${error.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error requesting documents:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsRequesting(false);
    }
  };

  const getConfidenceColor = (score) => {
    if (score >= 0.8) return '#48bb78';
    if (score >= 0.6) return '#ed8936';
    return '#f56565';
  };

  const getConfidenceLabel = (score) => {
    if (score >= 0.8) return 'High';
    if (score >= 0.6) return 'Medium';
    return 'Low';
  };

  return (
    <div className="profile-container">
      <div className="profile-header">
        <button className="back-btn" onClick={onBack}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1>Candidate Profile</h1>
      </div>

      <div className="profile-content">
        {/* Candidate Summary Card */}
        <div className="summary-card">
          <div className="profile-avatar-large">
            <FaUser size={40} />
          </div>
          <div className="summary-info">
            <h2>{candidate.name}</h2>
            <p className="summary-email"><FaEnvelope /> {candidate.email}</p>
            <p className="summary-company"><FaMapMarkerAlt /> {candidate.extractedData?.location || 'Not available'}</p>
            <div className="summary-status">
              <span className={`status-badge status-${candidate.extractionStatus.toLowerCase()}`}>
                {candidate.extractionStatus}
              </span>
            </div>
          </div>
        </div>

        {/* Extracted Data Section */}
        <div className="extracted-data-section">
          <h3>Extracted Information</h3>
          
          <div className="data-grid">
            {/* Personal Information */}
            <div className="data-card">
              <div className="data-card-header">
                <h4><FaUser /> Personal Information</h4>
              </div>
              <div className="data-items">
                <div className="data-item">
                  <label>Full Name:</label>
                  <span>{candidate.extractedData?.fullName || candidate.name}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.fullName || 0.95) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.fullName || 0.95)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.fullName || 0.95)} 
                      ({((candidate.extractedData?.confidence?.fullName || 0.95) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>

                <div className="data-item">
                  <label>Email:</label>
                  <span>{candidate.email}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.email || 0.98) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.email || 0.98)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.email || 0.98)} 
                      ({((candidate.extractedData?.confidence?.email || 0.98) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>

                <div className="data-item">
                  <label>Phone:</label>
                  <span>{candidate.extractedData?.phone || 'Not available'}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.phone || 0.85) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.phone || 0.85)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.phone || 0.85)} 
                      ({((candidate.extractedData?.confidence?.phone || 0.85) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>

                <div className="data-item">
                  <label>Location:</label>
                  <span>{candidate.extractedData?.location || 'Not available'}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.location || 0.75) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.location || 0.75)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.location || 0.75)} 
                      ({((candidate.extractedData?.confidence?.location || 0.75) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Professional Information */}
            <div className="data-card">
              <div className="data-card-header">
                <h4><FaBriefcase /> Professional Information</h4>
              </div>
              <div className="data-items">
                <div className="data-item">
                  <label>Current Company:</label>
                  <span>{candidate.company}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.company || 0.92) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.company || 0.92)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.company || 0.92)} 
                      ({((candidate.extractedData?.confidence?.company || 0.92) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>

                <div className="data-item">
                  <label>Position:</label>
                  <span>{candidate.extractedData?.position || 'Not available'}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.position || 0.88) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.position || 0.88)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.position || 0.88)} 
                      ({((candidate.extractedData?.confidence?.position || 0.88) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>

                <div className="data-item">
                  <label>Skills:</label>
                  <div className="skills-tags">
                    {(candidate.extractedData?.skills || ['JavaScript', 'React', 'Node.js']).map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.skills || 0.82) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.skills || 0.82)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.skills || 0.82)} 
                      ({((candidate.extractedData?.confidence?.skills || 0.82) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Education */}
            <div className="data-card">
              <div className="data-card-header">
                <h4><FaGraduationCap /> Education</h4>
              </div>
              <div className="data-items">
                <div className="data-item">
                  <label>Degree:</label>
                  <span>{candidate.extractedData?.degree || 'Not available'}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.degree || 0.90) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.degree || 0.90)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.degree || 0.90)} 
                      ({((candidate.extractedData?.confidence?.degree || 0.90) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>

                <div className="data-item">
                  <label>University:</label>
                  <span>{candidate.extractedData?.university || 'Not available'}</span>
                  <div className="confidence-indicator">
                    <span 
                      className="confidence-bar" 
                      style={{ 
                        width: `${(candidate.extractedData?.confidence?.university || 0.87) * 100}%`,
                        backgroundColor: getConfidenceColor(candidate.extractedData?.confidence?.university || 0.87)
                      }}
                    ></span>
                    <span className="confidence-score">
                      {getConfidenceLabel(candidate.extractedData?.confidence?.university || 0.87)} 
                      ({((candidate.extractedData?.confidence?.university || 0.87) * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="action-section">
          <button 
            className="request-docs-btn" 
            onClick={handleRequestDocuments}
            disabled={isRequesting}
          >
            <FaPaperPlane /> {isRequesting ? 'Sending Request...' : 'Request Additional Documents'}
          </button>
          <button className="view-docs-btn" onClick={() => setShowDocuments(!showDocuments)}>
            {showDocuments ? <><FaEyeSlash /> Hide</> : <><FaEye /> View</>} Submitted Documents
          </button>
        </div>

        {/* Document Section */}
        {showDocuments && (
          <DocumentSection 
            candidateId={candidate.id} 
            documents={candidate.submittedDocuments || candidate.documents || []}
            onDocumentsUpdate={async () => {
              // Refresh candidate data after document upload
              if (onRequestDocuments) {
                await onRequestDocuments(candidate.id);
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default CandidateProfile;
