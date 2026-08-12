import React from 'react';
import { DashboardCard } from './DashboardCard';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  headerAction?: React.ReactNode;
  height?: string;
  className?: string;
}

export const ChartCard: React.FC<ChartCardProps> = ({
  title,
  subtitle,
  children,
  headerAction,
  height = 'h-72',
  className = '',
}) => {
  return (
    <DashboardCard title={title} subtitle={subtitle} headerAction={headerAction} className={className}>
      <div className={`w-full ${height} flex items-center justify-center`}>
        {children}
      </div>
    </DashboardCard>
  );
};
