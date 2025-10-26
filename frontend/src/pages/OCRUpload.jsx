import { useState } from 'react';
import axiosInstance from '../api/axios';

function OCRUpload() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ocrData, setOcrData] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (selectedFile) => {
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setError(null);
    setOcrData(null);
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleScan = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axiosInstance.post('/api/ocr/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setOcrData({
        id: response.data.id,
        doctor_name: response.data.doctor_name || '',
        medications: response.data.medications || [{ name: '', dosage: '', frequency: '' }],
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to scan prescription');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setOcrData({ ...ocrData, [field]: value });
  };

  const handleMedicationChange = (index, field, value) => {
    const updatedMeds = [...ocrData.medications];
    updatedMeds[index][field] = value;
    setOcrData({ ...ocrData, medications: updatedMeds });
  };

  const addMedication = () => {
    setOcrData({
      ...ocrData,
      medications: [...ocrData.medications, { name: '', dosage: '', frequency: '' }],
    });
  };

  const removeMedication = (index) => {
    const updatedMeds = ocrData.medications.filter((_, i) => i !== index);
    setOcrData({ ...ocrData, medications: updatedMeds });
  };

  const handleSave = async () => {
    setLoading(true);
    setError(null);

    try {
      const endpoint = ocrData.id
        ? `/api/prescriptions/${ocrData.id}/`
        : '/api/prescriptions/';
      const method = ocrData.id ? 'patch' : 'post';

      await axiosInstance[method](endpoint, {
        doctor_name: ocrData.doctor_name,
        medications: ocrData.medications,
      });

      setError(null);
      alert('Prescription saved successfully!');
      setFile(null);
      setPreview(null);
      setOcrData(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save prescription');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-6">OCR Upload</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="fileInput"
            className="hidden"
            accept="image/*"
            onChange={handleFileInput}
          />
          <label htmlFor="fileInput" className="cursor-pointer">
            <div className="text-gray-500">
              <svg
                className="mx-auto h-12 w-12 text-gray-400 mb-4"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <p className="text-lg">Drop prescription image here or click to upload</p>
              <p className="text-sm text-gray-400 mt-2">PNG, JPG up to 10MB</p>
            </div>
          </label>
        </div>

        {preview && (
          <div className="mt-6">
            <p className="text-sm font-medium text-gray-700 mb-2">Preview:</p>
            <img
              src={preview}
              alt="Preview"
              className="max-h-64 mx-auto rounded border"
            />
            <button
              onClick={handleScan}
              disabled={loading}
              className="mt-4 w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <svg
                    className="animate-spin h-5 w-5 mr-2"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Scanning...
                </>
              ) : (
                'Scan Prescription'
              )}
            </button>
          </div>
        )}
      </div>

      {ocrData && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Extracted Information</h3>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Doctor Name
            </label>
            <input
              type="text"
              value={ocrData.doctor_name}
              onChange={(e) => handleInputChange('doctor_name', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter doctor name"
            />
          </div>

          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-gray-700">
                Medications
              </label>
              <button
                onClick={addMedication}
                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                + Add Medication
              </button>
            </div>

            {ocrData.medications.map((med, index) => (
              <div
                key={index}
                className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3 p-4 border border-gray-200 rounded-lg"
              >
                <input
                  type="text"
                  value={med.name}
                  onChange={(e) =>
                    handleMedicationChange(index, 'name', e.target.value)
                  }
                  className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Medication name"
                />
                <input
                  type="text"
                  value={med.dosage}
                  onChange={(e) =>
                    handleMedicationChange(index, 'dosage', e.target.value)
                  }
                  className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Dosage (e.g., 500mg)"
                />
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={med.frequency}
                    onChange={(e) =>
                      handleMedicationChange(index, 'frequency', e.target.value)
                    }
                    className="flex-1 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Frequency (e.g., 2x daily)"
                  />
                  {ocrData.medications.length > 1 && (
                    <button
                      onClick={() => removeMedication(index)}
                      className="px-3 py-2 text-red-600 hover:bg-red-50 rounded"
                    >
                      ✕
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={handleSave}
            disabled={loading}
            className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Saving...' : 'Save Prescription'}
          </button>
        </div>
      )}
    </div>
  );
}

export default OCRUpload;