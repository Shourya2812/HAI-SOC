import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from 'recharts';
import { RiskDistributionItem } from '../../types/index';

interface RiskDistributionChartProps {
  data: RiskDistributionItem[];
}

export const RiskDistributionChart: React.FC<RiskDistributionChartProps> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={55}
          outerRadius={85}
          paddingAngle={4}
          dataKey="count"
          nameKey="category"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color || '#3B82F6'} stroke="#0F172A" strokeWidth={2} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderRadius: '8px',
            color: '#F8FAFC',
            fontSize: '12px',
          }}
          formatter={(value: any, name: any, item: any) => [
            `${value} anomalies (${item.payload.percentage}%)`,
            name,
          ]}
        />
        <Legend
          verticalAlign="bottom"
          height={36}
          wrapperStyle={{ fontSize: '11px', color: '#94A3B8' }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
};
