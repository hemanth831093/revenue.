import React from 'react';
import { CheckCircle2, XCircle, Clock, ShieldAlert } from 'lucide-react';

interface Props {
  status: string;
}

export const StatusBadge: React.FC<Props> = ({ status }) => {
  const s = status.toUpperCase();

  if (s === 'RECOVERED' || s === 'SUCCESS') {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
        <CheckCircle2 className="w-3.5 h-3.5" />
        RECOVERED
      </span>
    );
  } else if (s === 'ESCALATED') {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/15 text-purple-400 border border-purple-500/30">
        <ShieldAlert className="w-3.5 h-3.5" />
        ESCALATED
      </span>
    );
  } else if (s === 'IN_PROGRESS' || s === 'PENDING') {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/15 text-blue-400 border border-blue-500/30">
        <Clock className="w-3.5 h-3.5 animate-spin" />
        IN PROGRESS
      </span>
    );
  } else {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/30">
        <XCircle className="w-3.5 h-3.5" />
        FAILED
      </span>
    );
  }
};
