import React from 'react';

interface DashboardCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  headerAction?: React.ReactNode;
  className?: string;
}

export const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  subtitle,
  children,
  headerAction,
  className = '',
}) => {
  return (
    <div
      className={`bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-lg backdrop-blur-md transition-all duration-200 hover:border-slate-700 ${className}`}
    >
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800/80">
        <div>
          <h3 className="text-sm font-semibold tracking-wide text-slate-100 flex items-center gap-2">
            <span className="w-1.5 h-4 bg-cyan-500 rounded-full inline-block"></span>
            {title}
          </h3>
          {subtitle && <p className="text-xs text-slate-400 mt-0.5 ml-3.5">{subtitle}</p>}
        </div>
        {headerAction && <div>{headerAction}</div>}
      </div>
      <div>{children}</div>
    </div>
  );
};
