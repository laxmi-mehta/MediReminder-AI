import { useState } from 'react';

function ExtractedResults({ data, onSave }) {
  const [formData, setFormData] = useState({
    prescription_id: data.prescription_id || null,
    doctor_name: data.doctor_name || '',
    medications: data.medications && data.medications.length > 0 
      ? data.medications 
      : [{ name: '', dosage: '', frequency: '' }],
  });

  const handleDoctorChange = (value) => {
    setFormData({ ...formData, doctor_name: value });
  };

  const handleMedicationChange = (index, field, value) => {
    const updatedMeds = [...formData.medications];
    updatedMeds[index][field] = value;
    setFormData({ ...formData, medications: updatedMeds });
  };

  const addRow = () => {
    setFormData({
      ...formData,
      medications: [...formData.medications, { name: '', dosage: '', frequency: '' }],
    });
  };

  const removeRow = (index) => {
    if (formData.medications.length === 1) return;
    const updatedMeds = formData.medications.filter((_, i) => i !== index);
    setFormData({ ...formData, medications: updatedMeds });
  };

  const handleSave = () => {
    onSave(formData);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Extracted Prescription Data</h3>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Doctor Name
        </label>
        <input
          type="text"
          value={formData.doctor_name}
          onChange={(e) => handleDoctorChange(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter doctor name"
        />
      </div>

      <div className="mb-4">
        <div className="flex justify-between items-center mb-3">
          <label className="block text-sm font-medium text-gray-700">
            Medications
          </label>
          <button
            onClick={addRow}
            className="flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            <span className="text-lg">+</span> Add Row
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-b">
                  Medication Name
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-b">
                  Dosage
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-b">
                  Frequency
                </th>
                <th className="px-4 py-3 text-center text-xs font-medium text-gray-700 uppercase tracking-wider border-b">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {formData.medications.map((med, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <input
                      type="text"
                      value={med.name}
                      onChange={(e) => handleMedicationChange(index, 'name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., Aspirin"
                    />
                  </td>
                  <td className="px-4 py-3">
                    <input
                      type="text"
                      value={med.dosage}
                      onChange={(e) => handleMedicationChange(index, 'dosage', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 500mg"
                    />
                  </td>
                  <td className="px-4 py-3">
                    <input
                      type="text"
                      value={med.frequency}
                      onChange={(e) => handleMedicationChange(index, 'frequency', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 2x daily"
                    />
                  </td>
                  <td className="px-4 py-3 text-center">
                    <button
                      onClick={() => removeRow(index)}
                      disabled={formData.medications.length === 1}
                      className="text-red-600 hover:text-red-700 disabled:text-gray-400 disabled:cursor-not-allowed px-2 py-1"
                      title="Remove row"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <button
        onClick={handleSave}
        className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-medium"
      >
        Save Prescription
      </button>
    </div>
  );
}

export default ExtractedResults;