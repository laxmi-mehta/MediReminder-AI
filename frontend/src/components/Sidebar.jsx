import { NavLink } from 'react-router-dom';

function Sidebar() {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/medications', label: 'Medications', icon: '💊' },
    { path: '/reminders', label: 'Reminders', icon: '⏰' },
    { path: '/ocr-upload', label: 'OCR Upload', icon: '📄' },
  ];

  return (
    <aside className="w-64 bg-white shadow-lg">
      <div className="p-6">
        <h2 className="text-xl font-bold text-blue-600">MediReminder</h2>
      </div>
      <nav className="mt-6">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors ${
                isActive ? 'bg-blue-50 text-blue-600 border-r-4 border-blue-600' : ''
              }`
            }
          >
            <span className="mr-3 text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;