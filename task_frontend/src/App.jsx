import { useState, useEffect } from 'react';
import ResumeUpload from './components/ResumeUpload';
import CandidateDashboard from './components/CandidateDashboard';
import CandidateProfile from './components/CandidateProfile';
import './App.css';

function App() {
  const [view, setView] = useState('dashboard'); // 'dashboard' or 'profile'
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch candidates from backend
  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      const response = await fetch('https://ai-agent-bcg-1-flask.onrender.com/api/candidates');
      if (response.ok) {
        const data = await response.json();
        setCandidates(data);
      }
    } catch (error) {
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  // OLD Mock data - keeping as comment for reference
  /*const [candidates, setCandidates] = useState([
    {
      id: 1,
      name: 'John Doe',
      email: 'john.doe@example.com',
      company: 'Tech Corp',
      extractionStatus: 'Completed',
      uploadDate: '2025-11-20',
      extractedData: {
        fullName: 'John Doe',
        phone: '+1 234-567-8900',
        location: 'San Francisco, CA',
        position: 'Senior Software Engineer',
        experience: '5 years',
        skills: ['JavaScript', 'React', 'Node.js', 'Python'],
        degree: 'Bachelor of Computer Science',
        university: 'Stanford University',
        confidence: {
          fullName: 0.95,
          email: 0.98,
          phone: 0.85,
          location: 0.75,
          company: 0.92,
          position: 0.88,
          experience: 0.70,
          skills: 0.82,
          degree: 0.90,
          university: 0.87
        }
      },
      documents: [
        {
          id: 101,
          name: 'Resume.pdf',
          type: 'application/pdf',
          size: 245678,
          uploadDate: '2025-11-20',
          status: 'Uploaded'
        }
      ]
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane.smith@example.com',
      company: 'Digital Solutions',
      extractionStatus: 'Processing',
      uploadDate: '2025-11-25',
      extractedData: {
        fullName: 'Jane Smith',
        phone: '+1 987-654-3210',
        location: 'New York, NY',
        position: 'Product Manager',
        experience: '7 years',
        skills: ['Product Management', 'Agile', 'Scrum', 'User Research'],
        degree: 'MBA',
        university: 'Harvard Business School',
        confidence: {
          fullName: 0.96,
          email: 0.99,
          phone: 0.88,
          location: 0.82,
          company: 0.93,
          position: 0.90,
          experience: 0.78,
          skills: 0.85,
          degree: 0.92,
          university: 0.89
        }
      },
      documents: []
    },
    {
      id: 3,
      name: 'Mike Johnson',
      email: 'mike.j@example.com',
      company: 'StartupXYZ',
      extractionStatus: 'Pending',
      uploadDate: '2025-11-27',
      extractedData: {
        fullName: 'Mike Johnson',
        phone: '+1 555-123-4567',
        location: 'Austin, TX',
        position: 'DevOps Engineer',
        experience: '4 years',
        skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
        degree: 'Bachelor of Engineering',
        university: 'MIT',
        confidence: {
          fullName: 0.94,
          email: 0.97,
          phone: 0.80,
          location: 0.73,
          company: 0.90,
          position: 0.86,
          experience: 0.68,
          skills: 0.79,
          degree: 0.88,
          university: 0.85
        }
      },
      documents: []
    }
  ]);*/

  const handleUploadSuccess = async (result) => {
    // Refresh candidates list after successful upload
    await fetchCandidates();
    alert('Resume uploaded and processed successfully!');
  };

  const handleCandidateSelect = async (candidate) => {
    // Fetch full candidate details from backend
    try {
      const response = await fetch(`https://ai-agent-bcg-1-flask.onrender.com/api/candidates/${candidate.id}`);
      if (response.ok) {
        const fullCandidate = await response.json();
        setSelectedCandidate(fullCandidate);
        setView('profile');
      }
    } catch (error) {
      console.error('Error fetching candidate details:', error);
      alert('Failed to load candidate details');
    }
  };

  const handleBackToDashboard = () => {
    setView('dashboard');
    setSelectedCandidate(null);
    fetchCandidates(); // Refresh the list
  };

  const handleRequestDocuments = async (candidateId) => {
    // TODO: Implement actual API call to send document request email
    console.log('Requesting documents for candidate:', candidateId);
    return Promise.resolve();
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">🎯 TraqCheck</h1>
          <p className="app-subtitle">Resume Extraction & Document Management System</p>
        </div>
      </header>

      <main className="app-main">
        {view === 'dashboard' ? (
          <>
            <ResumeUpload onUploadSuccess={handleUploadSuccess} />
            <CandidateDashboard 
              candidates={candidates} 
              onCandidateSelect={handleCandidateSelect} 
            />
          </>
        ) : (
          <CandidateProfile 
            candidate={selectedCandidate}
            onBack={handleBackToDashboard}
            onRequestDocuments={handleRequestDocuments}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>© 2025 TraqCheck. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
