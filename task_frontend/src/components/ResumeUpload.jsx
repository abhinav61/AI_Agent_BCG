import { useState, useRef } from 'react';
import { FaFileUpload, FaFilePdf, FaFileWord } from 'react-icons/fa';
import './ResumeUpload.css';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file) => {
    // Validate file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF or Word document');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setUploadedFile(file);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 15;
        });
      }, 300);

      const formData = new FormData();
      formData.append('resume', file);
      
      const response = await fetch('https://ai-agent-bcg.onrender.com/api/candidates/upload', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.ok) {
        const result = await response.json();
        setTimeout(() => {
          setIsUploading(false);
          setUploadProgress(0);
          setUploadedFile(null);
          if (onUploadSuccess) {
            onUploadSuccess(result);
          }
        }, 500);
      } else {
        const error = await response.json();
        throw new Error(error.error || 'Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert(`Upload failed: ${error.message}`);
      setIsUploading(false);
      setUploadProgress(0);
      setUploadedFile(null);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="resume-upload-container">
      <div
        className={`upload-dropzone ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        {!isUploading ? (
          <>
            <div className="upload-icon"><FaFileUpload size={50} /></div>
            <h3>Upload Resume</h3>
            <p>Drag and drop a resume here, or</p>
            <button className="browse-btn" onClick={handleBrowseClick}>
              Browse Files
            </button>
            <p className="file-types">Supported formats: PDF, DOC, DOCX</p>
          </>
        ) : (
          <div className="upload-progress">
            <div className="upload-file-info">
              <span className="file-icon"><FaFilePdf size={24} /></span>
              <span className="file-name">{uploadedFile?.name}</span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="progress-text">{uploadProgress}% uploaded</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeUpload;
