import React, { useState } from 'react';
import axios from 'axios';

interface FileUploadProps {
  label: string;
  onUploadSuccess: (fileId: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ label, onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('applicantName', 'Applicant'); // This should come from form state

    try {
      setUploading(true);
      setMessage('');
      const response = await axios.post('/api/applications/upload', formData);
      
      setMessage('✅ Document uploaded successfully!');
      onUploadSuccess(response.data.fileId);
    } catch (error) {
      setMessage('❌ Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <label>{label}</label>
      <input 
        type="file" 
        onChange={handleFileChange} 
        disabled={uploading}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />
      {uploading && <p className="text-sm text-blue-500">Uploading...</p>}
      {message && <p className={`text-sm ${message.includes('✅') ? 'text-green-500' : 'text-red-500'}`}>{message}</p>}
    </div>
  );
};
