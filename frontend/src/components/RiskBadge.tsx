import React from 'react';
import { AlertTriangle, AlertCircle, ShieldCheck } from 'lucide-react';

interface Props {
  priority?: string;
  probability?: number;
}

export const RiskBadge: React.FC<Props> = ({ priority = 'MEDIUM', probability }) => {
  const p = priority.toUpperCase();
  
  if (p === 'HIGH') {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
        <ShieldCheck className="w-3.5 h-3.5" />
        HIGH PRIORITY {probability !== undefined ? `(${Math.round(probability * 100)}%)` : ''}
      </span>
    );
  } else if (p === 'MEDIUM') {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">
        <AlertTriangle className="w-3.5 h-3.5" />
        MEDIUM {probability !== undefined ? `(${Math.round(probability * 100)}%)` : ''}
      </span>
    );
  } else {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-500/10 text-slate-400 border border-slate-500/30">
        <AlertCircle className="w-3.5 h-3.5" />
        LOW {probability !== undefined ? `(${Math.round(probability * 100)}%)` : ''}
      </span>
    );
  }
};
