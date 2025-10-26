import { useState } from 'react';

function MedicationForm({ initialData, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    dosage: initialData?.dosage || '',
    frequency: initialData?.frequency || '',
    start_date: initialData?.start_date || '',
    end_date: initialData?.end_date || '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.dosage.trim()) newErrors.dosage = 'Dosage is required';
    if (!formData.frequency.trim()) newErrors.frequency = 'Frequency is required';
    if (formData.start_date && formData.end_date && formData.end_date < formData.start_date) {
      newErrors.end_date = 'End date must be after start date';
    }
    return newErrors;
  };

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
    if (errors[field]) {
      setErrors({ ...errors, [field]: null });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    try {
      await onSubmit(formData);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        {initialData ? 'Edit Medication' : 'Add New Medication'}
      </h3>
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.name ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., Aspirin"
            />
            {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dosage <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.dosage}
              onChange={(e) => handleChange('dosage', e.target.value)}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.dosage ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., 500mg"
            />
            {errors.dosage && <p className="text-red-500 text-xs mt-1">{errors.dosage}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Frequency <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.frequency}
              onChange={(e) => handleChange('frequency', e.target.value)}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.frequency ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., 2x daily"
            />
            {errors.frequency && <p className="text-red-500 text-xs mt-1">{errors.frequency}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
            <input
              type="date"
              value={formData.start_date}
              onChange={(e) => handleChange('start_date', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
            <input
              type="date"
              value={formData.end_date}
              onChange={(e) => handleChange('end_date', e.target.value)}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.end_date ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.end_date && <p className="text-red-500 text-xs mt-1">{errors.end_date}</p>}
          </div>
        </div>

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
          >
            {loading ? 'Saving...' : initialData ? 'Update' : 'Add'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default MedicationForm;