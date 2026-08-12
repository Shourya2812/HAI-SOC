import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

export const AppLayout: React.FC = () => {
  const [collapsedSidebar, setCollapsedSidebar] = useState(false);
  const [selectedHospital, setSelectedHospital] = useState('St. Jude Medical Center (Central)');

  return (
    <div className="min-h-screen bg-[#090D16] text-slate-100 flex flex-col font-sans antialiased soc-grid-bg">
      <div className="flex flex-1 overflow-hidden">
        {/* Navigation Sidebar */}
        <Sidebar
          collapsed={collapsedSidebar}
          onToggleCollapse={() => setCollapsedSidebar(!collapsedSidebar)}
        />

        {/* Main Content Workspace */}
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          <Navbar
            selectedHospital={selectedHospital}
            onSelectHospital={setSelectedHospital}
            onToggleSidebar={() => setCollapsedSidebar(!collapsedSidebar)}
          />

          <main className="flex-1 p-6 space-y-6">
            <Outlet context={{ selectedHospital }} />
          </main>
        </div>
      </div>
    </div>
  );
};
