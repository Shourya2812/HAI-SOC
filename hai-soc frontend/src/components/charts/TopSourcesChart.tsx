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
import { LogSourceMetric } from '../../types/index';

interface TopSourcesChartProps {
  data: LogSourceMetric[];
}

export const TopSourcesChart: React.FC<TopSourcesChartProps> = ({ data }) => {
  const COLORS = ['#3B82F6', '#06B6D4', '#8B5CF6', '#F59E0B', '#10B981'];

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={data}
        layout="vertical"
        margin={{ top: 5, right: 20, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" horizontal={false} />
        <XAxis type="number" stroke="#64748B" fontSize={11} tickLine={false} />
        <YAxis
          type="category"
          dataKey="source"
          stroke="#94A3B8"
          fontSize={11}
          tickLine={false}
          width={130}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderRadius: '8px',
            color: '#F8FAFC',
            fontSize: '12px',
          }}
          formatter={(value: any, name: any) => [
            typeof value === 'number' ? value.toLocaleString() + ' logs' : value,
            'Ingested Volume',
          ]}
        />
        <Bar dataKey="count" radius={[0, 4, 4, 0]}>
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
