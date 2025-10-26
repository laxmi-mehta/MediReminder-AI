import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import OCRUpload from './pages/OCRUpload';
import Medications from './pages/Medications';
import Reminders from './pages/Reminders';

function App() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm px-6 py-4">
          <h1 className="text-2xl font-semibold text-gray-800">MediReminder</h1>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ocr" element={<OCRUpload />} />
            <Route path="/medications" element={<Medications />} />
            <Route path="/reminders" element={<Reminders />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;