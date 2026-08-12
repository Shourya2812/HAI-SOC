import React, { useState } from 'react';
import {
  Search,
  Bell,
  Building2,
  Clock,
  User,
  CheckCircle2,
  AlertCircle,
  Menu,
} from 'lucide-react';
import { useIntervalClock } from '../../hooks/useSocData';

interface NavbarProps {
  selectedHospital: string;
  onSelectHospital: (hospital: string) => void;
  onToggleSidebar: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  selectedHospital,
  onSelectHospital,
  onToggleSidebar,
}) => {
  const currentTime = useIntervalClock();
  const [showNotifications, setShowNotifications] = useState(false);
  const [globalQuery, setGlobalQuery] = useState('');

  const hospitals = [
    'St. Jude Medical Center (Central)',
    'Mayo Regional Clinic (East Wing)',
    'Johns Hopkins Trauma Unit',
    'Cleveland Clinic Childrens',
    'All Healthcare Sites (Group View)',
  ];

  const notifications = [
    {
      id: 1,
      time: '2 mins ago',
      type: 'CRITICAL',
      title: 'Bulk PHI Export Anomaly Flagged',
      desc: 'Cardiology EHR flagged 1,400 record exports by dr.a.chen',
    },
    {
      id: 2,
      time: '15 mins ago',
      type: 'HIGH',
      title: 'IoMT Infusion Pump Payload Unregistered',
      desc: 'Unsigned firmware modification payload blocked on Emergency VLAN',
    },
    {
      id: 3,
      time: '1 hour ago',
      type: 'INFO',
      title: 'HIPAA Automated Audit Sync Complete',
      desc: '164.312(a)(1) compliance rating updated to 98%',
    },
  ];

  return (
    <header className="h-16 bg-slate-950/90 border-b border-slate-800/80 px-4 flex items-center justify-between sticky top-0 z-20 backdrop-blur-md">
      {/* Left: Sidebar Toggle & Hospital Selector */}
      <div className="flex items-center gap-4">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 border border-transparent hover:border-slate-800 transition-colors"
          title="Toggle Navigation Sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Hospital Selector */}
        <div className="relative flex items-center gap-2 px-3 py-1.5 bg-slate-900/80 border border-slate-800 rounded-xl">
          <Building2 className="w-4 h-4 text-cyan-400 shrink-0" />
          <select
            value={selectedHospital}
            onChange={(e) => onSelectHospital(e.target.value)}
            className="bg-transparent text-xs font-semibold text-slate-200 focus:outline-none cursor-pointer pr-2 font-mono"
          >
            {hospitals.map((h) => (
              <option key={h} value={h} className="bg-slate-900 text-slate-200">
                {h}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Middle: Global Search */}
      <div className="hidden md:flex items-center relative w-96">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <input
          type="text"
          value={globalQuery}
          onChange={(e) => setGlobalQuery(e.target.value)}
          placeholder="Global SOC search (IP, EHR User, Incident ID, Hash, Device MAC)..."
          className="w-full pl-9 pr-4 py-1.5 bg-slate-900/90 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-mono"
        />
        <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-mono text-slate-500 border border-slate-800 px-1.5 py-0.5 rounded">
          ⌘K
        </span>
      </div>

      {/* Right: Clock, Notifications, System Status, User Profile */}
      <div className="flex items-center gap-4">
        {/* UTC Live Clock */}
        <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-900/60 border border-slate-800/80 font-mono text-xs text-slate-300">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span>{currentTime || 'Syncing UTC...'}</span>
        </div>

        {/* Notifications Dropdown Toggle */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition-colors relative"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500"></span>
          </button>

          {/* Notifications Popover */}
          {showNotifications && (
            <div className="absolute right-0 mt-3 w-80 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl z-50 p-4 space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-slate-100 uppercase font-mono">
                  Security Alerts
                </span>
                <span className="text-[10px] bg-red-950 text-red-400 px-2 py-0.5 rounded font-mono">
                  3 New
                </span>
              </div>

              <div className="space-y-2 max-h-64 overflow-y-auto">
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold text-red-400 font-mono flex items-center gap-1">
                        <AlertCircle className="w-3 h-3" />
                        {n.title}
                      </span>
                      <span className="text-[9px] text-slate-500 font-mono">{n.time}</span>
                    </div>
                    <p className="text-[11px] text-slate-300">{n.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* System Health Pill */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/60 text-emerald-400 text-[11px] font-mono font-semibold">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>SOC Protected</span>
        </div>

        {/* User Profile */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold text-xs shadow-md border border-cyan-400/30">
            <User className="w-4 h-4" />
          </div>
          <div className="hidden xl:block text-left">
            <div className="text-xs font-bold text-slate-200">Dr. Elena Rostova</div>
            <div className="text-[10px] text-cyan-400 font-mono">Senior Lead Analyst</div>
          </div>
        </div>
      </div>
    </header>
  );
};
