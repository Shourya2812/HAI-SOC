import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from 'recharts';
import { DepartmentDistribution } from '../../types/index';

interface DepartmentRiskChartProps {
  data: DepartmentDistribution[];
}

export const DepartmentRiskChart: React.FC<DepartmentRiskChartProps> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
        <XAxis
          dataKey="department"
          stroke="#94A3B8"
          fontSize={10}
          tickLine={false}
          angle={-15}
          textAnchor="end"
        />
        <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
        <Tooltip
          contentStyle={{
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderRadius: '8px',
            color: '#F8FAFC',
            fontSize: '12px',
          }}
          formatter={(value: any) => [
            `${value} logs`,
            'Log Count',
          ]}
        />
        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color || '#10B981'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
