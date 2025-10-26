import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axios';

function Dashboard() {
  const [todaysReminders, setTodaysReminders] = useState([]);
  const [recentMedications, setRecentMedications] = useState([]);
  const [stats, setStats] = useState({
    totalMedications: 0,
    activeReminders: 0,
    upcomingDoses: 0,
  });
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      const [remindersRes, medicationsRes] = await Promise.all([
        axiosInstance.get('/api/reminders/'),
        axiosInstance.get('/api/medications/'),
      ]);

      const today = new Date().toISOString().split('T')[0];
      const todayReminders = remindersRes.data.filter((r) => {
        const reminderDate = new Date(r.scheduled_time).toISOString().split('T')[0];
        return reminderDate === today && !r.is_done;
      });

      const recentMeds = medicationsRes.data.slice(0, 5);

      const upcomingCount = remindersRes.data.filter((r) => {
        return new Date(r.scheduled_time) > new Date() && !r.is_done;
      }).length;

      setTodaysReminders(todayReminders);
      setRecentMedications(recentMeds);
      setStats({
        totalMedications: medicationsRes.data.length,
        activeReminders: remindersRes.data.filter((r) => !r.is_done).length,
        upcomingDoses: upcomingCount,
      });
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type.startsWith('image/')) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleQuickScan = async () => {
    if (!file) return;

    setUploadLoading(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      await axiosInstance.post('/api/ocr/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      navigate('/ocr');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to scan prescription');
    } finally {
      setUploadLoading(false);
    }
  };

  const markReminderDone = async (id) => {
    try {
      await axiosInstance.patch(`/api/reminders/${id}/`, { is_done: true });
      setTodaysReminders(todaysReminders.filter((r) => r.id !== id));
      setStats({ ...stats, activeReminders: stats.activeReminders - 1 });
    } catch (err) {
      alert('Failed to mark reminder as done');
    }
  };

  const formatTime = (dateTime) => {
    return new Date(dateTime).toLocaleTimeString('en-US', {
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
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Dashboard</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Medications</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalMedications}</p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <span className="text-3xl">💊</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Active Reminders</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.activeReminders}</p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <span className="text-3xl">⏰</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Upcoming Doses</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.upcomingDoses}</p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <span className="text-3xl">📅</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Today's Reminders</h3>
            <Link to="/reminders" className="text-sm text-blue-600 hover:text-blue-700">
              View All
            </Link>
          </div>

          {todaysReminders.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No reminders for today</p>
              <p className="text-sm mt-2">You're all caught up! 🎉</p>
            </div>
          ) : (
            <div className="space-y-3">
              {todaysReminders.map((reminder) => (
                <div
                  key={reminder.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      onChange={() => markReminderDone(reminder.id)}
                      className="h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
                    />
                    <div>
                      <p className="font-medium text-gray-900">
                        {reminder.medication_name || `Medication ${reminder.medication}`}
                      </p>
                      <p className="text-sm text-gray-600">{formatTime(reminder.scheduled_time)}</p>
                    </div>
                  </div>
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                    {reminder.repeat || 'one-time'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick OCR Scan</h3>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                id="quickScanInput"
                className="hidden"
                accept="image/*"
                onChange={handleFileSelect}
              />
              <label htmlFor="quickScanInput" className="cursor-pointer">
                {preview ? (
                  <img src={preview} alt="Preview" className="max-h-32 mx-auto rounded mb-3" />
                ) : (
                  <div className="text-gray-400 mb-3">
                    <svg
                      className="mx-auto h-12 w-12"
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
                  </div>
                )}
                <p className="text-sm text-gray-600">
                  {preview ? 'Click to change image' : 'Click to upload prescription'}
                </p>
              </label>
            </div>

            <button
              onClick={handleQuickScan}
              disabled={!file || uploadLoading}
              className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {uploadLoading ? 'Scanning...' : 'Scan & Extract'}
            </button>

            <Link
              to="/ocr"
              className="block w-full text-center text-sm text-blue-600 hover:text-blue-700"
            >
              Go to full OCR page →
            </Link>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Recent Medications</h3>
          <Link to="/medications" className="text-sm text-blue-600 hover:text-blue-700">
            View All
          </Link>
        </div>

        {recentMedications.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No medications added yet</p>
            <Link to="/medications" className="text-sm text-blue-600 hover:text-blue-700 mt-2 inline-block">
              Add your first medication
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                    Name
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                    Dosage
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                    Frequency
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {recentMedications.map((med) => (
                  <tr key={med.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{med.name}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">{med.dosage}</td>
                    <td className="px-4 py-3 text-sm text-gray-700">{med.frequency}</td>
                    <td className="px-4 py-3 text-sm">
                      {med.end_date && new Date(med.end_date) < new Date() ? (
                        <span className="bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs">
                          Expired
                        </span>
                      ) : (
                        <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">
                          Active
                        </span>
                      )}
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

export default Dashboard;