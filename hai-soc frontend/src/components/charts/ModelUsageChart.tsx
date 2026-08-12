import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from 'recharts';
import { ModelUsageMetric } from '../../types/index';

interface ModelUsageChartProps {
  data: ModelUsageMetric[];
}

export const ModelUsageChart: React.FC<ModelUsageChartProps> = ({ data }) => {
  const COLORS = ['#8B5CF6', '#06B6D4', '#3B82F6', '#EC4899', '#10B981'];

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={85}
          paddingAngle={5}
          dataKey="usagePercentage"
          nameKey="modelName"
        >
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="#0F172A" strokeWidth={2} />
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
            `${value}% usage (${item.payload.inferencesToday?.toLocaleString()} inferences)`,
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
