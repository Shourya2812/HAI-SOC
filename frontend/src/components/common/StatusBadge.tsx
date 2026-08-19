import React from 'react';
import { IncidentStatus } from '../../types/index';
import { getStatusBgColor } from '../../utils/formatters';

interface StatusBadgeProps {
  status: IncidentStatus | string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const badgeClass = getStatusBgColor(status as IncidentStatus);

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-semibold border tracking-wider uppercase font-mono ${badgeClass}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5 animate-pulse"></span>
      {status}
    </span>
  );
};
