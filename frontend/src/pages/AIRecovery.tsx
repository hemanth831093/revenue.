import React, { useState, useEffect } from 'react';
import { Bot, Zap, RefreshCw, CheckCircle2, ShieldAlert, ArrowRight } from 'lucide-react';
import { getTransactions, batchExecuteRecovery, executeRecoveryAction } from '../services/api';
import { Transaction } from '../types';
import { RiskBadge } from '../components/RiskBadge';

interface Props {
  onSelectTransaction: (id: number) => void;
}

export const AIRecovery: React.FC<Props> = ({ onSelectTransaction }) => {
  const [highPriorityItems, setHighPriorityItems] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [batchExecuting, setBatchExecuting] = useState(false);
  const [batchSummary, setBatchSummary] = useState<any>(null);

  const loadHighPriorityCases = async () => {
    setLoading(true);
    try {
      // Fetch failed transactions with HIGH priority
      const res = await getTransactions({
        status: 'FAILED',
        priority: 'HIGH',
        limit: 50
      });
      setHighPriorityItems(res.items);
    } catch (e) {
      console.error('Failed to load high priority cases', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHighPriorityCases();
  }, []);

  const handleRunBatch = async () => {
    if (highPriorityItems.length === 0) return;
    setBatchExecuting(true);
    try {
      const ids = highPriorityItems.map(t => t.id);
      const res = await batchExecuteRecovery(ids);
      setBatchSummary(res);
      await loadHighPriorityCases();
    } catch (e: any) {
      alert("Batch execution error: " + (e.message || "Error"));
    } finally {
      setBatchExecuting(false);
    }
  };

  const handleSingleExecute = async (id: number) => {
    try {
      await executeRecoveryAction(id);
      await loadHighPriorityCases();
    } catch (e: any) {
      alert("Execution error: " + (e.message || "Error"));
    }
  };

  const totalAtRisk = highPriorityItems.reduce((acc, item) => acc + item.amount, 0);

  return (
    <div className="space-y-8">
      {/* Page Header & Batch Action Trigger */}
      <div className="p-8 rounded-3xl glass-panel border border-indigo-500/20 bg-gradient-to-r from-indigo-950/60 via-slate-900 to-slate-950 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
            <Bot className="w-3.5 h-3.5" />
            Autonomous AI Recovery Queue
          </div>
          <h1 className="text-3xl font-black text-white">High-Priority Payment Recovery</h1>
          <p className="text-sm text-slate-300 leading-relaxed">
            Diagnosed by Scikit-learn Risk Engine with <strong className="text-emerald-400">$\ge 70\%$ recovery probability</strong>. Total recoverable revenue at risk: <strong className="text-indigo-400">₹{totalAtRisk.toLocaleString('en-IN')}</strong> across {highPriorityItems.length} cases.
          </p>
        </div>

        <button
          onClick={handleRunBatch}
          disabled={batchExecuting || highPriorityItems.length === 0}
          className="px-6 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-extrabold text-xs shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 disabled:opacity-50 transition-all shrink-0"
        >
          {batchExecuting ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              Running Batch Recovery...
            </>
          ) : (
            <>
              <Zap className="w-4 h-4 fill-current text-amber-300" />
              Batch Auto-Recover ({highPriorityItems.length} Cases)
            </>
          )}
        </button>
      </div>

      {/* Batch Execution Notification Banner */}
      {batchSummary && (
        <div className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 text-xs flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
            <div>
              <span className="font-bold">Batch Recovery Execution Finished!</span> Processed {batchSummary.processed_count} high-priority cases cleanly.
            </div>
          </div>
          <button onClick={() => setBatchSummary(null)} className="text-xs font-bold text-slate-400 hover:text-white">Dismiss</button>
        </div>
      )}

      {/* Queue Table */}
      <div className="rounded-2xl glass-panel border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-900/60 text-[11px] font-extrabold uppercase tracking-wider text-slate-400">
                <th className="py-4 px-6">Payment ID</th>
                <th className="py-4 px-6">Customer</th>
                <th className="py-4 px-6">Amount</th>
                <th className="py-4 px-6">Failure Reason</th>
                <th className="py-4 px-6">Recovery Prob.</th>
                <th className="py-4 px-6">Recommended Action</th>
                <th className="py-4 px-6 text-right">Quick Execute</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto text-indigo-400 mb-2" />
                    Scanning queue for high-priority cases...
                  </td>
                </tr>
              ) : highPriorityItems.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500 font-semibold">
                    No high-priority failed transactions currently in queue. All high recovery cases resolved!
                  </td>
                </tr>
              ) : (
                highPriorityItems.map((tx) => {
                  const recAction = tx.failure_reason === 'card_expired' ? 'PAYMENT_LINK' : (tx.failure_reason === 'insufficient_funds' ? 'REMINDER' : 'RETRY');
                  return (
                    <tr key={tx.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-4 px-6 font-mono text-indigo-300 font-bold">{tx.payment_id}</td>
                      <td className="py-4 px-6">
                        <div className="font-semibold text-white">{tx.customer_name}</div>
                        <div className="text-[10px] text-slate-500">{tx.customer_email}</div>
                      </td>
                      <td className="py-4 px-6 font-extrabold text-white">₹{tx.amount.toLocaleString('en-IN')}</td>
                      <td className="py-4 px-6 font-mono text-slate-400">{tx.failure_reason}</td>
                      <td className="py-4 px-6">
                        <RiskBadge priority="HIGH" probability={tx.recovery_probability || 0.87} />
                      </td>
                      <td className="py-4 px-6 font-extrabold text-emerald-400">
                        {recAction}
                      </td>
                      <td className="py-4 px-6 text-right space-x-2">
                        <button
                          onClick={() => handleSingleExecute(tx.id)}
                          className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-emerald-600 text-white font-extrabold text-xs shadow-md hover:from-indigo-500 hover:to-emerald-500 inline-flex items-center gap-1.5"
                        >
                          <Zap className="w-3.5 h-3.5 fill-current" />
                          Execute
                        </button>
                        <button
                          onClick={() => onSelectTransaction(tx.id)}
                          className="px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 hover:text-white font-semibold text-xs"
                        >
                          Inspect
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
