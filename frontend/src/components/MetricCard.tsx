import React from 'react';
import { LucideIcon } from 'lucide-react';

interface Props {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
  trendPositive?: boolean;
  accentColor?: 'indigo' | 'emerald' | 'amber' | 'rose' | 'purple';
}

export const MetricCard: React.FC<Props> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendPositive = true,
  accentColor = 'indigo'
}) => {
  const colorClasses = {
    indigo: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20 glow-indigo',
    emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20 glow-emerald',
    amber: 'text-amber-400 bg-amber-500/10 border-amber-500/20 glow-amber',
    rose: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20'
  };

  return (
    <div className={`p-6 rounded-2xl glass-panel glass-panel-hover border flex flex-col justify-between ${colorClasses[accentColor]}`}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400">{title}</span>
        <div className={`p-2.5 rounded-xl ${colorClasses[accentColor]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="mt-4">
        <div className="text-3xl font-extrabold tracking-tight text-white font-sans">{value}</div>
        {subtitle && <div className="text-xs text-slate-400 mt-1">{subtitle}</div>}
      </div>
      {trend && (
        <div className="mt-3 flex items-center text-xs font-semibold">
          <span className={trendPositive ? 'text-emerald-400' : 'text-rose-400'}>
            {trend}
          </span>
          <span className="text-slate-500 ml-1">vs last period</span>
        </div>
      )}
    </div>
  );
};
