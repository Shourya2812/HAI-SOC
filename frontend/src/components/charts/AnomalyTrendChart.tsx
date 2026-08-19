import React from 'react';

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { DailyTrend } from '../../types/index';

interface AnomalyTrendChartProps {
  data: DailyTrend[];
}

export const AnomalyTrendChart: React.FC<AnomalyTrendChartProps> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id="colorAnomalies" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.4} />
            <stop offset="95%" stopColor="#06B6D4" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="colorBaseline" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#64748B" stopOpacity={0.2} />
            <stop offset="95%" stopColor="#64748B" stopOpacity={0} />
          </linearGradient>
        </defs>

        <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
        <XAxis dataKey="hour" stroke="#64748B" fontSize={11} tickLine={false} />
        <YAxis stroke="#64748B" fontSize={11} tickLine={false} />

        <Tooltip
          contentStyle={{
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderRadius: '8px',
            color: '#F8FAFC',
            fontSize: '12px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)',
          }}
          itemStyle={{ color: '#E2E8F0' }}
        />

        <Legend
          verticalAlign="top"
          align="right"
          wrapperStyle={{ fontSize: '11px', color: '#94A3B8', paddingBottom: '10px' }}
        />

        <Area
          type="monotone"
          dataKey="baseline"
          name="Baseline Normal"
          stroke="#64748B"
          fillOpacity={1}
          fill="url(#colorBaseline)"
          strokeDasharray="4 4"
        />
        <Area
          type="monotone"
          dataKey="anomalies"
          name="ML Anomalies"
          stroke="#06B6D4"
          strokeWidth={2}
          fillOpacity={1}
          fill="url(#colorAnomalies)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};
