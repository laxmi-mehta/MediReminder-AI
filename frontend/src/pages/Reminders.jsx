import { useState, useEffect } from 'react';
import axiosInstance from '../api/axios';

function Reminders() {
  const [reminders, setReminders] = useState([]);
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    medication: '',
    scheduled_time: '',
    repeat: 'none',
  });
  const [formErrors, setFormErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchReminders();
    fetchMedications();
  }, []);

  const fetchReminders = async () => {
    try {
      setLoading(true);
      const response = await axiosInstance.get('/api/reminders/');
      setReminders(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch reminders');
    } finally {
      setLoading(false);
    }
  };

  const fetchMedications = async () => {
    try {
      const response = await axiosInstance.get('/api/medications/');
      setMedications(response.data);
    } catch (err) {
      console.error('Failed to fetch medications:', err);
    }
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.medication) errors.medication = 'Please select a medication';
    if (!formData.scheduled_time) errors.scheduled_time = 'Please select date and time';
    return errors;
  };

  const handleFormChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
    if (formErrors[field]) {
      setFormErrors({ ...formErrors, [field]: null });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setSubmitting(true);
    try {
      const response = await axiosInstance.post('/api/reminders/', formData);
      setReminders([...reminders, response.data]);
      setFormData({ medication: '', scheduled_time: '', repeat: 'none' });
      setShowForm(false);
      setFormErrors({});
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to create reminder');
    } finally {
      setSubmitting(false);
    }
  };

  const toggleDone = async (id, currentStatus) => {
    try {
      const response = await axiosInstance.patch(`/api/reminders/${id}/`, {
        is_done: !currentStatus,
      });
      setReminders(reminders.map((r) => (r.id === id ? response.data : r)));
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to update reminder');
    }
  };

  const handleSendTest = async (id) => {
    try {
      await axiosInstance.post(`/api/reminders/${id}/send_test/`);
      alert('Test reminder sent successfully!');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to send test reminder');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this reminder?')) return;

    try {
      await axiosInstance.delete(`/api/reminders/${id}/`);
      setReminders(reminders.filter((r) => r.id !== id));
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete reminder');
    }
  };

  const formatDateTime = (dateTime) => {
    return new Date(dateTime).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
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
        <h2 className="text-2xl font-semibold text-gray-800">Reminders</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          {showForm ? 'Cancel' : '+ Schedule Reminder'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Schedule New Reminder</h3>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Medication <span className="text-red-500">*</span>
                </label>
                <select
                  value={formData.medication}
                  onChange={(e) => handleFormChange('medication', e.target.value)}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    formErrors.medication ? 'border-red-500' : 'border-gray-300'
                  }`}
                >
                  <option value="">Select a medication</option>
                  {medications.map((med) => (
                    <option key={med.id} value={med.id}>
                      {med.name} - {med.dosage}
                    </option>
                  ))}
                </select>
                {formErrors.medication && (
                  <p className="text-red-500 text-xs mt-1">{formErrors.medication}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Scheduled Time <span className="text-red-500">*</span>
                </label>
                <input
                  type="datetime-local"
                  value={formData.scheduled_time}
                  onChange={(e) => handleFormChange('scheduled_time', e.target.value)}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    formErrors.scheduled_time ? 'border-red-500' : 'border-gray-300'
                  }`}
                />
                {formErrors.scheduled_time && (
                  <p className="text-red-500 text-xs mt-1">{formErrors.scheduled_time}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Repeat
                </label>
                <select
                  value={formData.repeat}
                  onChange={(e) => handleFormChange('repeat', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="none">None (One-time)</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              {submitting ? 'Creating...' : 'Create Reminder'}
            </button>
          </form>
        </div>
      )}

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {reminders.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No reminders scheduled. Click "Schedule Reminder" to add one.
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {reminders.map((reminder) => (
              <div
                key={reminder.id}
                className={`p-6 hover:bg-gray-50 transition-colors ${
                  reminder.is_done ? 'bg-gray-50 opacity-75' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4 flex-1">
                    <input
                      type="checkbox"
                      checked={reminder.is_done || false}
                      onChange={() => toggleDone(reminder.id, reminder.is_done)}
                      className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
                    />
                    <div className="flex-1">
                      <h4
                        className={`text-lg font-medium ${
                          reminder.is_done ? 'line-through text-gray-500' : 'text-gray-900'
                        }`}
                      >
                        {reminder.medication_name || `Medication ID: ${reminder.medication}`}
                      </h4>
                      <div className="mt-2 space-y-1 text-sm text-gray-600">
                        <p>
                          <span className="font-medium">Time:</span>{' '}
                          {formatDateTime(reminder.scheduled_time)}
                        </p>
                        <p>
                          <span className="font-medium">Repeat:</span>{' '}
                          <span className="capitalize">{reminder.repeat || 'none'}</span>
                        </p>
                        {reminder.is_done && (
                          <p className="text-green-600">
                            <span className="font-medium">✓ Completed</span>
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <button
                      onClick={() => handleSendTest(reminder.id)}
                      className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                      title="Send test notification"
                    >
                      Send Test
                    </button>
                    <button
                      onClick={() => handleDelete(reminder.id)}
                      className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
                      title="Delete reminder"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Reminders;