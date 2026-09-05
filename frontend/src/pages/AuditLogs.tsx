import React, { useState, useEffect } from 'react';
import { FileCheck2, Search, RefreshCw, ChevronLeft, ChevronRight, ShieldCheck } from 'lucide-react';
import { getAuditLogs } from '../services/api';
import { AuditLog } from '../types';

export const AuditLogs: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [actionType, setActionType] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await getAuditLogs({
        search,
        action_type: actionType || undefined,
        page,
        limit: 15
      });
      setLogs(res.items);
      setTotalPages(res.total_pages);
      setTotalCount(res.total);
    } catch (e) {
      console.error('Failed to fetch audit logs', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [search, actionType, page]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2">
            <FileCheck2 className="w-6 h-6 text-indigo-400" />
            Autonomous Decision Audit Logs
          </h1>
          <p className="text-xs text-slate-400">
            Immutable timeline of all AI diagnoses, stopping rules evaluated, and Razorpay sandbox executions ({totalCount} entries)
          </p>
        </div>
        <button
          onClick={fetchLogs}
          className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 text-xs font-bold"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh Audit Trail
        </button>
      </div>

      {/* Filter Bar */}
      <div className="p-4 rounded-2xl glass-panel border border-slate-800 flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
          <input
            type="text"
            placeholder="Search Decision, Payment ID, Reason..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <select
          value={actionType}
          onChange={(e) => { setActionType(e.target.value); setPage(1); }}
          className="px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
        >
          <option value="">All Action Types</option>
          <option value="RETRY">RETRY</option>
          <option value="PAYMENT_LINK">PAYMENT_LINK</option>
          <option value="REMINDER">REMINDER</option>
          <option value="HUMAN_ESCALATION">HUMAN_ESCALATION</option>
        </select>
      </div>

      {/* Table */}
      <div className="rounded-2xl glass-panel border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-900/60 text-[11px] font-extrabold uppercase tracking-wider text-slate-400">
                <th className="py-4 px-6">Timestamp</th>
                <th className="py-4 px-6">Payment ID</th>
                <th className="py-4 px-6">Customer</th>
                <th className="py-4 px-6">Decision</th>
                <th className="py-4 px-6">Reason Explanation</th>
                <th className="py-4 px-6">Action Taken</th>
                <th className="py-4 px-6">Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto text-indigo-400 mb-2" />
                    Fetching audit logs...
                  </td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500 font-semibold">
                    No audit records match filters.
                  </td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-mono text-[11px] text-slate-400">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="py-4 px-6 font-mono text-indigo-300 font-bold">{log.payment_id || 'N/A'}</td>
                    <td className="py-4 px-6 font-semibold text-white">{log.customer_name || 'N/A'}</td>
                    <td className="py-4 px-6 font-mono text-xs text-indigo-400">{log.decision}</td>
                    <td className="py-4 px-6 max-w-xs truncate text-slate-300" title={log.reason}>
                      {log.reason}
                    </td>
                    <td className="py-4 px-6 font-bold text-white">{log.action_taken}</td>
                    <td className="py-4 px-6">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-extrabold ${log.execution_result === 'SUCCESS' ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30' : 'bg-purple-500/15 text-purple-400 border border-purple-500/30'}`}>
                        {log.execution_result}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        <div className="p-4 border-t border-slate-800/80 bg-slate-900/40 flex items-center justify-between text-xs text-slate-400">
          <div>
            Showing page <strong className="text-white">{page}</strong> of <strong className="text-white">{totalPages}</strong>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page === 1}
              className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white disabled:opacity-40"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page === totalPages}
              className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white disabled:opacity-40"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
