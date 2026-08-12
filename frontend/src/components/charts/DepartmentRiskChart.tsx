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
import { DepartmentMetric } from '../../types/index';

interface DepartmentRiskChartProps {
  data: DepartmentMetric[];
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
        <YAxis stroke="#64748B" fontSize={11} tickLine={false} domain={[0, 100]} />
        <Tooltip
          contentStyle={{
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderRadius: '8px',
            color: '#F8FAFC',
            fontSize: '12px',
          }}
          formatter={(value: any, name: any) => [
            `${value} / 100`,
            'Department Risk Index',
          ]}
        />
        <Bar dataKey="riskScore" radius={[4, 4, 0, 0]}>
          {data.map((entry, index) => {
            const color =
              entry.riskScore > 80
                ? '#EF4444'
                : entry.riskScore > 60
                ? '#F59E0B'
                : '#10B981';
            return <Cell key={`cell-${index}`} fill={color} />;
          })}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
