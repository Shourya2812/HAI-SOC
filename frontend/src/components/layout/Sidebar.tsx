import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  AlertTriangle,
  BrainCircuit,
  ShieldAlert,
  Grid,
  FileCheck2,
  Workflow,
  Settings,
  Activity,
  HeartPulse,
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ collapsed }) => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Logs', path: '/logs', icon: FileText },
    { name: 'Incidents', path: '/incidents', icon: AlertTriangle, badge: '18' },
    { name: 'Anomaly Detection', path: '/anomalies', icon: BrainCircuit },
    { name: 'Threat Intelligence', path: '/threat-intel', icon: ShieldAlert },
    { name: 'MITRE ATT&CK', path: '/mitre', icon: Grid },
    { name: 'HIPAA Compliance', path: '/hipaa', icon: FileCheck2 },
    { name: 'Playbooks', path: '/playbooks', icon: Workflow },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside
      className={`bg-slate-950 border-r border-slate-800/80 flex flex-col transition-all duration-300 z-30 ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 px-4 flex items-center justify-between border-b border-slate-800/80 bg-slate-950/80">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 text-white shadow-[0_0_15px_rgba(6,182,212,0.4)]">
            <HeartPulse className="w-5 h-5 animate-pulse" />
          </div>
          {!collapsed && (
            <div>
              <h1 className="font-extrabold text-sm tracking-wider text-white font-mono flex items-center gap-1.5">
                HAI-SOC
                <span className="text-[9px] bg-cyan-950 text-cyan-400 border border-cyan-800/60 px-1.5 py-0.2 rounded font-sans uppercase">
                  Enterprise
                </span>
              </h1>
              <p className="text-[10px] text-slate-400 truncate">Healthcare AI SOC</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] uppercase font-mono text-slate-500 px-3 mb-2 tracking-widest">
          {!collapsed ? 'Core Operations' : '•••'}
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 group ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-950/80 to-blue-950/50 text-cyan-400 border border-cyan-800/60 shadow-[0_0_15px_-3px_rgba(6,182,212,0.25)]'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/80 hover:border hover:border-slate-800'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <Icon className="w-4 h-4 shrink-0 transition-transform group-hover:scale-110" />
                {!collapsed && <span>{item.name}</span>}
              </div>

              {!collapsed && item.badge && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-red-950 text-red-400 border border-red-800/60 font-mono">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950/90">
        {!collapsed ? (
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400 animate-pulse" />
              <div>
                <p className="text-[11px] font-bold text-slate-200">ML Engine Active</p>
                <p className="text-[9px] text-slate-400">0.4ms avg inference</p>
              </div>
            </div>
            <span className="w-2 h-2 rounded-full bg-emerald-400 glow-cyan"></span>
          </div>
        ) : (
          <div className="flex justify-center py-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 glow-cyan" title="ML Engine Active"></span>
          </div>
        )}
      </div>
    </aside>
  );
};
