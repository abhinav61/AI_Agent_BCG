import { useState, useRef, useEffect } from 'react';
import { FaFilePdf, FaFileWord, FaFileImage, FaFile, FaDownload, FaTrash, FaInbox } from 'react-icons/fa';
import './DocumentSection.css';

const DocumentSection = ({ candidateId, documents, onDocumentsUpdate }) => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [localDocuments, setLocalDocuments] = useState(documents || []);
  const [documentType, setDocumentType] = useState('pan_card'); // pan_card or aadhaar_card
  const fileInputRef = useRef(null);

  // Update local documents when props change
  useEffect(() => {
    setLocalDocuments(documents || []);
  }, [documents]);

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      // Validate file type
      const file = files[0];
      const allowedTypes = ['application/pdf', 'application/msword', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/png', 'image/jpeg', 'image/jpg'];
      
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(pdf|doc|docx|png|jpg|jpeg)$/i)) {
        alert('Invalid file type. Please upload PDF, DOC, DOCX, PNG, or JPEG files only.');
        return;
      }
      
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file) => {
    setIsUploading(true);
    setUploadProgress(0);
    setUploadedFile(file);

    const formData = new FormData();
    formData.append(documentType, file);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await fetch(`http://localhost:5000/api/candidates/${candidateId}/submit-documents`, {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.ok) {
        const data = await response.json();
        setTimeout(() => {
          setIsUploading(false);
          setUploadProgress(0);
          setUploadedFile(null);
          
          // Refresh the documents list by calling parent callback
          if (onDocumentsUpdate) {
            onDocumentsUpdate();
          } else {
            // Fallback: add to local state
            setLocalDocuments([...localDocuments, {
              id: Date.now(),
              name: file.name,
              type: file.type,
              size: file.size,
              uploadDate: new Date().toISOString(),
              status: 'Submitted'
            }]);
          }
          
          alert(data.message || 'Document uploaded successfully!');
        }, 500);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert(error.message || 'Upload failed. Please try again.');
      setIsUploading(false);
      setUploadProgress(0);
      setUploadedFile(null);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleDownload = (document) => {
    // TODO: Implement actual download
    console.log('Downloading:', document.name);
    alert(`Downloading ${document.name}...`);
  };

  const handleDelete = (documentId) => {
    if (confirm('Are you sure you want to delete this document?')) {
      // TODO: Implement actual delete API call
      setLocalDocuments(localDocuments.filter(doc => doc.id !== documentId));
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getFileIcon = (type) => {
    if (type.includes('pdf')) return <FaFilePdf size={24} />;
    if (type.includes('word') || type.includes('document')) return <FaFileWord size={24} />;
    if (type.includes('image')) return <FaFileImage size={24} />;
    return <FaFile size={24} />;
  };

  return (
    <div className="document-section">
      <h3>Submitted Documents</h3>

      {/* Documents List */}
      <div className="documents-list">
        {localDocuments.length === 0 ? (
          <div className="no-documents">
            <FaInbox className="no-docs-icon" size={48} />
            <p>No documents uploaded yet</p>
          </div>
        ) : (
          localDocuments.map((doc) => (
            <div key={doc.id} className="document-item">
              <div className="document-icon">
                {getFileIcon(doc.type || doc.name)}
              </div>
              <div className="document-info">
                <div className="document-name">
                  {doc.name}
                  {doc.documentType && (
                    <span style={{ marginLeft: '8px', fontSize: '12px', color: '#666' }}>
                      ({doc.documentType})
                    </span>
                  )}
                </div>
                <div className="document-meta">
                  {formatFileSize(doc.size)} • Uploaded {new Date(doc.uploadDate).toLocaleDateString()}
                  {doc.documentNumber && (
                    <span style={{ marginLeft: '8px', fontSize: '11px', color: '#555', fontWeight: '600' }}>
                      • Number: {doc.documentNumber}
                    </span>
                  )}
                  {doc.extractedName && (
                    <span style={{ marginLeft: '8px', fontSize: '11px', color: '#888' }}>
                      • Name: {doc.extractedName}
                    </span>
                  )}
                  {doc.similarityScore !== undefined && (
                    <span style={{ marginLeft: '8px', fontSize: '11px', color: '#888' }}>
                      • Match: {(doc.similarityScore * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
              </div>
              <div className="document-status">
                <span className={`status-badge-small ${
                  doc.verificationStatus === 'Pass' ? 'status-completed' : 
                  doc.verificationStatus === 'Verification Failed' ? 'status-failed' : 
                  'status-uploaded'
                }`}>
                  {doc.verificationStatus || doc.status || 'Uploaded'}
                </span>
              </div>
              <div className="document-actions">
                <button 
                  className="action-btn download-btn" 
                  onClick={() => handleDownload(doc)}
                  title="Download"
                >
                  <FaDownload />
                </button>
                <button 
                  className="action-btn delete-btn" 
                  onClick={() => handleDelete(doc.id)}
                  title="Delete"
                >
                  <FaTrash />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default DocumentSection;
