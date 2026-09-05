import React, { useEffect, useState } from 'react';
import { BarChart3, TrendingUp, DollarSign, Zap, Activity } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { getDashboardMetrics } from '../services/api';
import { DashboardMetrics } from '../types';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];

export const Analytics: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardMetrics().then(data => {
      setMetrics(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading || !metrics) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Activity className="w-8 h-8 text-indigo-400 animate-spin" />
      </div>
    );
  }

  const actionEfficiencyData = [
    { name: 'RETRY (Gateway)', value: 45 },
    { name: 'PAYMENT_LINK', value: 30 },
    { name: 'REMINDER', value: 15 },
    { name: 'HUMAN_ESCALATION', value: 10 }
  ];

  const trendData = [
    { day: 'Mon', recovered: 12500, risk: 45000 },
    { day: 'Tue', recovered: 18400, risk: 42000 },
    { day: 'Wed', recovered: 24000, risk: 38000 },
    { day: 'Thu', recovered: 31500, risk: 35000 },
    { day: 'Fri', recovered: 42000, risk: 29000 },
    { day: 'Sat', recovered: 51200, risk: 24000 },
    { day: 'Sun', recovered: 68500, risk: 18000 }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-black text-white flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-indigo-400" />
          Recovery Performance Analytics
        </h1>
        <p className="text-xs text-slate-400">Deep telemetry analytics across payment failure categories, recovery efficiency, and revenue trend</p>
      </div>

      {/* Grid 1: Daily Revenue Trend Area Chart */}
      <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            7-Day Recovered Revenue Trajectory
          </h3>
          <span className="text-xs text-slate-400 font-mono">Live Telemetry</span>
        </div>
        <div className="h-72 w-full pt-4">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="colorRec" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} tickFormatter={(v) => `₹${v / 1000}k`} />
              <Tooltip contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
              <Area type="monotone" dataKey="recovered" name="Recovered Revenue (₹)" stroke="#10b981" fillOpacity={1} fill="url(#colorRec)" strokeWidth={3} />
              <Area type="monotone" dataKey="risk" name="Revenue at Risk (₹)" stroke="#f43f5e" fillOpacity={1} fill="url(#colorRisk)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Grid 2: Reason Bar Chart & Action Efficiency Donut Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recovery by Failure Reason */}
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-indigo-400" />
            Failure Reasons Breakdown
          </h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={metrics.chart_reason_data}>
                <XAxis dataKey="reason" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Bar dataKey="count" fill="#6366f1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Action Efficiency Pie */}
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-amber-400" />
            Recovery Action Type Efficiency (%)
          </h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={actionEfficiencyData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={5}
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {actionEfficiencyData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
