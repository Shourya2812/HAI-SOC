import React from 'react';
import { SeverityLevel } from '../../types/index';
import { getSeverityBgColor } from '../../utils/formatters';

interface SeverityBadgeProps {
  severity: SeverityLevel | string;
}

export const SeverityBadge: React.FC<SeverityBadgeProps> = ({ severity }) => {
  const badgeClass = getSeverityBgColor(severity as SeverityLevel);

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-semibold border tracking-wider uppercase font-mono ${badgeClass}`}
    >
      {severity}
    </span>
  );
};
