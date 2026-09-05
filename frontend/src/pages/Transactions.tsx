import React, { useState, useEffect } from 'react';
import { Search, Filter, RefreshCw, ChevronLeft, ChevronRight, Eye, Bot, Receipt } from 'lucide-react';
import { getTransactions, analyzeTransaction } from '../services/api';
import { Transaction, AIAnalysis } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';
import { AIAnalysisModal } from '../components/AIAnalysisModal';

interface Props {
  onSelectTransaction: (id: number) => void;
}

export const Transactions: React.FC<Props> = ({ onSelectTransaction }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [reason, setReason] = useState('');
  const [priority, setPriority] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Modal State
  const [selectedAnalysis, setSelectedAnalysis] = useState<AIAnalysis | null>(null);

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const res = await getTransactions({
        search,
        status: status || undefined,
        failure_reason: reason || undefined,
        priority: priority || undefined,
        page,
        limit: 10
      });
      setTransactions(res.items);
      setTotalPages(res.total_pages);
      setTotalCount(res.total);
    } catch (e) {
      console.error('Failed to fetch transactions', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [search, status, reason, priority, page]);

  const handleAnalyze = async (id: number) => {
    try {
      const res = await analyzeTransaction(id);
      setSelectedAnalysis(res);
    } catch (e) {
      alert("Failed to analyze transaction.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2">
            <Receipt className="w-6 h-6 text-indigo-400" />
            Payment Transactions Directory
          </h1>
          <p className="text-xs text-slate-400">Search, filter, and inspect failed or recovered merchant payments ({totalCount} total)</p>
        </div>
        <button
          onClick={fetchTransactions}
          className="p-2.5 rounded-xl glass-panel text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-2 text-xs font-bold"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Filter Controls Bar */}
      <div className="p-4 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Search Box */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
            <input
              type="text"
              placeholder="Search Payment ID, Customer..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          {/* Status Filter */}
          <select
            value={status}
            onChange={(e) => { setStatus(e.target.value); setPage(1); }}
            className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Statuses</option>
            <option value="FAILED">FAILED</option>
            <option value="RECOVERED">RECOVERED</option>
            <option value="ESCALATED">ESCALATED</option>
          </select>

          {/* Reason Filter */}
          <select
            value={reason}
            onChange={(e) => { setReason(e.target.value); setPage(1); }}
            className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Failure Reasons</option>
            <option value="bank_timeout">Bank Timeout</option>
            <option value="insufficient_funds">Insufficient Funds</option>
            <option value="card_expired">Card Expired</option>
            <option value="network_error">Network Error</option>
            <option value="fraud_flag">Fraud Flag</option>
          </select>

          {/* Priority Filter */}
          <select
            value={priority}
            onChange={(e) => { setPriority(e.target.value); setPage(1); }}
            className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Risk Priorities</option>
            <option value="HIGH">HIGH Priority</option>
            <option value="MEDIUM">MEDIUM Priority</option>
            <option value="LOW">LOW Priority</option>
          </select>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="rounded-2xl glass-panel border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-900/60 text-[11px] font-extrabold uppercase tracking-wider text-slate-400">
                <th className="py-4 px-6">Payment ID</th>
                <th className="py-4 px-6">Customer</th>
                <th className="py-4 px-6">Amount</th>
                <th className="py-4 px-6">Method</th>
                <th className="py-4 px-6">Failure Reason</th>
                <th className="py-4 px-6">Status</th>
                <th className="py-4 px-6">Recovery Prob.</th>
                <th className="py-4 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-500">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto text-indigo-400 mb-2" />
                    Fetching payment directory...
                  </td>
                </tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-500 font-semibold">
                    No transactions match your search filters.
                  </td>
                </tr>
              ) : (
                transactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-mono text-indigo-300 font-bold">{tx.payment_id}</td>
                    <td className="py-4 px-6">
                      <div className="font-semibold text-white">{tx.customer_name}</div>
                      <div className="text-[10px] text-slate-500">{tx.customer_email}</div>
                    </td>
                    <td className="py-4 px-6 font-extrabold text-white">₹{tx.amount.toLocaleString('en-IN')}</td>
                    <td className="py-4 px-6 font-medium text-slate-400">{tx.payment_method}</td>
                    <td className="py-4 px-6">
                      <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                        {tx.failure_reason}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <StatusBadge status={tx.status} />
                    </td>
                    <td className="py-4 px-6">
                      <RiskBadge priority={tx.priority} probability={tx.recovery_probability} />
                    </td>
                    <td className="py-4 px-6 text-right space-x-2">
                      <button
                        onClick={() => handleAnalyze(tx.id)}
                        className="px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 hover:bg-indigo-500/20 font-semibold text-xs inline-flex items-center gap-1"
                      >
                        <Bot className="w-3.5 h-3.5" />
                        AI Analyze
                      </button>
                      <button
                        onClick={() => onSelectTransaction(tx.id)}
                        className="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white font-semibold text-xs inline-flex items-center gap-1"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        View
                      </button>
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

      {/* AI Analysis Modal */}
      {selectedAnalysis && (
        <AIAnalysisModal
          analysis={selectedAnalysis}
          onClose={() => setSelectedAnalysis(null)}
          onSuccess={fetchTransactions}
        />
      )}
    </div>
  );
};
