import React, { useEffect, useState } from 'react';
import {
  TrendingUp,
  DollarSign,
  AlertCircle,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  Zap,
  Activity,
  Bot,
  Sparkles
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { getDashboardMetrics } from '../services/api';
import { DashboardMetrics } from '../types';
import { MetricCard } from '../components/MetricCard';

interface Props {
  onNavigateToRecovery: () => void;
  onSelectTransaction: (id: number) => void;
}

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6'];

export const Dashboard: React.FC<Props> = ({ onNavigateToRecovery, onSelectTransaction }) => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    try {
      const data = await getDashboardMetrics();
      setMetrics(data);
    } catch (err) {
      console.error('Failed to load dashboard metrics', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  if (loading || !metrics) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <Activity className="w-8 h-8 text-indigo-400 animate-spin" />
          <span className="text-sm font-semibold text-slate-400">Loading RecoverAI Analytics...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Hero Welcome Banner with Primary CTA */}
      <div className="relative overflow-hidden rounded-3xl glass-panel border border-indigo-500/20 p-8 bg-gradient-to-r from-indigo-950/60 via-slate-900/80 to-slate-950">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
              <Sparkles className="w-3.5 h-3.5" />
              Autonomous Payment Intelligence Active
            </div>
            <h1 className="text-3xl font-black tracking-tight text-white">
              Revenue Recovery Overview
            </h1>
            <p className="text-slate-300 text-sm leading-relaxed">
              RecoverAI has analyzed synthetic transaction telemetry and detected{' '}
              <strong className="text-emerald-400">₹{metrics.total_revenue_recovered.toLocaleString('en-IN')}</strong> in recovered merchant revenue with a{' '}
              <strong className="text-indigo-400">{metrics.recovery_rate}% recovery rate</strong>.
            </p>
          </div>

          <button
            onClick={onNavigateToRecovery}
            className="px-6 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-extrabold text-sm shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-3 group transition-all shrink-0"
          >
            <span>Review High-Priority Payments ({metrics.high_priority_count})</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Revenue at Risk"
          value={`₹${metrics.total_revenue_at_risk.toLocaleString('en-IN')}`}
          subtitle={`${metrics.failed_payments_count} failed payment transactions`}
          icon={AlertCircle}
          accentColor="rose"
        />
        <MetricCard
          title="Recovered Revenue"
          value={`₹${metrics.total_revenue_recovered.toLocaleString('en-IN')}`}
          subtitle={`${metrics.recovered_payments_count} recovered payments`}
          icon={CheckCircle2}
          accentColor="emerald"
          trend="+18.4%"
          trendPositive={true}
        />
        <MetricCard
          title="Recovery Rate"
          value={`${metrics.recovery_rate}%`}
          subtitle="Successful automated retries & links"
          icon={TrendingUp}
          accentColor="indigo"
          trend="+4.2%"
          trendPositive={true}
        />
        <MetricCard
          title="High Priority Cases"
          value={metrics.high_priority_count}
          subtitle="Top recoverable failed payments"
          icon={ShieldCheck}
          accentColor="amber"
        />
      </div>

      {/* Recharts Analytics Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue Breakdown */}
        <div className="lg:col-span-2 p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-emerald-400" />
              Revenue at Risk vs Recovered Revenue
            </h3>
            <span className="text-xs text-slate-400 font-mono">Live Telemetry</span>
          </div>
          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={metrics.chart_revenue_data}>
                <XAxis dataKey="category" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} tickFormatter={(v) => `₹${v / 1000}k`} />
                <Tooltip
                  formatter={(val: any) => [`₹${Number(val).toLocaleString('en-IN')}`, 'Amount']}
                  contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                />
                <Bar dataKey="amount" radius={[8, 8, 0, 0]}>
                  {metrics.chart_revenue_data.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={index === 0 ? '#f43f5e' : '#10b981'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Failure Reasons Breakdown */}
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-indigo-400" />
            Failure Reasons
          </h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={metrics.chart_reason_data}
                  dataKey="count"
                  nameKey="reason"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ reason }) => reason}
                >
                  {metrics.chart_reason_data.map((_, index) => (
                    <Cell key={`cell-pie-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ background: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent AI Actions Timeline Feed */}
      <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-indigo-400" />
            Recent AI Decision & Execution Log
          </h3>
          <span className="text-xs text-indigo-400 font-semibold">Unalterable Audit Feed</span>
        </div>

        <div className="space-y-3">
          {metrics.recent_actions.map((act) => (
            <div
              key={act.id}
              onClick={() => onSelectTransaction(act.transaction_id)}
              className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40 cursor-pointer flex items-center justify-between transition-all"
            >
              <div className="flex items-center gap-4">
                <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 font-mono text-xs font-bold">
                  {act.payment_id}
                </div>
                <div>
                  <div className="text-sm font-semibold text-white">{act.customer_name}</div>
                  <div className="text-xs text-slate-400">
                    Action: <strong className="text-indigo-300">{act.action_taken}</strong> • Result: <strong className={act.execution_result === 'SUCCESS' ? 'text-emerald-400' : 'text-purple-400'}>{act.execution_result}</strong>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <div className="text-sm font-extrabold text-white">₹{act.amount.toLocaleString('en-IN')}</div>
                <div className="text-[11px] text-slate-500 font-mono">
                  {new Date(act.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
