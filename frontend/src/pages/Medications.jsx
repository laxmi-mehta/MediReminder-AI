import { useState, useEffect } from 'react';
import axiosInstance from '../api/axios';
import MedicationForm from '../components/MedicationForm';

function Medications() {
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingMed, setEditingMed] = useState(null);

  useEffect(() => {
    fetchMedications();
  }, []);

  const fetchMedications = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.get('/api/medications/');
      setMedications(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch medications');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingMed(null);
    setShowForm(true);
  };

  const handleEdit = (med) => {
    setEditingMed(med);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this medication?')) return;

    try {
      await axiosInstance.delete(`/api/medications/${id}/`);
      setMedications(medications.filter((m) => m.id !== id));
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete medication');
    }
  };

  const handleFormSubmit = async (data) => {
    try {
      if (editingMed) {
        const response = await axiosInstance.put(`/api/medications/${editingMed.id}/`, data);
        setMedications(medications.map((m) => (m.id === editingMed.id ? response.data : m)));
      } else {
        const response = await axiosInstance.post('/api/medications/', data);
        setMedications([...medications, response.data]);
      }
      setShowForm(false);
      setEditingMed(null);
    } catch (err) {
      throw new Error(err.response?.data?.error || 'Failed to save medication');
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingMed(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-800">Medications</h2>
        <button
          onClick={handleAdd}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + Add Medication
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {showForm && (
        <div className="mb-6">
          <MedicationForm
            initialData={editingMed}
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
          />
        </div>
      )}

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {medications.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No medications found. Click "Add Medication" to get started.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                    Dosage
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                    Frequency
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                    Start Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                    End Date
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {medications.map((med) => (
                  <tr key={med.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{med.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-700">{med.dosage}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-700">{med.frequency}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-700">
                        {med.start_date ? new Date(med.start_date).toLocaleDateString() : '-'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-700">
                        {med.end_date ? new Date(med.end_date).toLocaleDateString() : '-'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleEdit(med)}
                        className="text-blue-600 hover:text-blue-900 mr-4"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(med.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Medications;