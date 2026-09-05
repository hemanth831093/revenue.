import React, { useState, useEffect } from 'react';
import { ArrowLeft, Bot, ShieldCheck, Zap, RefreshCw, CheckCircle2, Clock, User, CreditCard, AlertCircle } from 'lucide-react';
import { getTransactionDetail, analyzeTransaction, executeRecoveryAction } from '../services/api';
import { Transaction, AIAnalysis } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { RiskBadge } from '../components/RiskBadge';

interface Props {
  transactionId: number;
  onBack: () => void;
}

export const TransactionDetails: React.FC<Props> = ({ transactionId, onBack }) => {
  const [transaction, setTransaction] = useState<Transaction | null>(null);
  const [analysis, setAnalysis] = useState<AIAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [execResult, setExecResult] = useState<any>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const txData = await getTransactionDetail(transactionId);
      setTransaction(txData);
      const aiData = await analyzeTransaction(transactionId);
      setAnalysis(aiData);
    } catch (e) {
      console.error('Failed to load transaction details', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [transactionId]);

  const handleExecuteAction = async () => {
    if (!analysis) return;
    setExecuting(true);
    try {
      const res = await executeRecoveryAction(transactionId, analysis.recommended_action);
      setExecResult(res);
      await loadData();
    } catch (e: any) {
      alert("Failed to execute recovery action: " + (e.message || "Error"));
    } finally {
      setExecuting(false);
    }
  };

  if (loading || !transaction || !analysis) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <RefreshCw className="w-8 h-8 text-indigo-400 animate-spin" />
          <span className="text-sm font-semibold text-slate-400">Loading Transaction Details...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Top Back Navigation & Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl glass-panel text-slate-300 hover:text-white hover:bg-slate-800 text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Directory
        </button>
        <div className="flex items-center gap-3">
          <StatusBadge status={transaction.status} />
          <RiskBadge priority={analysis.priority} probability={analysis.recovery_probability} />
        </div>
      </div>

      {/* Main Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Customer & Payment Telemetry */}
        <div className="space-y-6">
          {/* Customer Info Card */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <User className="w-4 h-4 text-indigo-400" />
              Customer Profile
            </h3>
            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-500 block">Name</span>
                <span className="font-bold text-white text-sm">{transaction.customer_name}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Email</span>
                <span className="font-mono text-slate-300">{transaction.customer_email}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Customer ID</span>
                <span className="font-mono text-indigo-400">{transaction.customer_id}</span>
              </div>
              <div className="pt-2 border-t border-slate-800 flex justify-between">
                <div>
                  <span className="text-slate-500 block text-[11px]">Past Successes</span>
                  <span className="font-bold text-emerald-400 text-sm">{transaction.previous_successes}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[11px]">Past Failures</span>
                  <span className="font-bold text-rose-400 text-sm">{transaction.previous_failures}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[11px]">Retries</span>
                  <span className="font-bold text-amber-400 text-sm">{transaction.retry_count}/3</span>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Telemetry Card */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <CreditCard className="w-4 h-4 text-indigo-400" />
              Payment Details
            </h3>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-slate-500">Payment ID</span>
                <span className="font-mono text-indigo-300 font-bold">{transaction.payment_id}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500">Amount</span>
                <span className="font-extrabold text-white text-base">₹{transaction.amount.toLocaleString('en-IN')}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500">Method</span>
                <span className="font-semibold text-slate-300">{transaction.payment_method}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500">Failure Code</span>
                <span className="font-mono text-rose-400">{transaction.failure_code || transaction.failure_reason}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Middle & Right Columns: AI Diagnosis, Safety Rules & Bounded Action Trigger */}
        <div className="lg:col-span-2 space-y-6">
          {/* AI Risk Score Gauge & Diagnosis Card */}
          <div className="p-6 rounded-2xl glass-panel border border-indigo-500/20 bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/40 space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                  <Bot className="w-6 h-6" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-white">AI Diagnosis & Risk Scoring</h2>
                  <span className="text-xs text-slate-400">Scikit-learn Model Engine v1.0</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-3xl font-black text-emerald-400">{Math.round(analysis.recovery_probability * 100)}%</div>
                <div className="text-[11px] text-slate-400">Recovery Likelihood</div>
              </div>
            </div>

            {/* Root Cause Diagnosis Box */}
            <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/30 space-y-1">
              <div className="font-bold text-indigo-300 text-sm">{analysis.diagnosis}</div>
              <p className="text-xs text-slate-300 leading-relaxed">{analysis.diagnosis_explanation}</p>
            </div>

            {/* Risk Signals */}
            <div className="space-y-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Signal Evidence</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                {analysis.risk_factors.map((rf, i) => (
                  <div key={i} className="p-2.5 rounded-lg bg-slate-800/60 border border-slate-700 text-slate-300">
                    • {rf}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Safety Check Summary */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Safety Bounded Rules Check
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-slate-500 block text-[11px]">Max Retries</span>
                <span className="font-bold text-white mt-0.5 block">{transaction.retry_count} / 3</span>
                <span className={transaction.retry_count >= 3 ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                  {transaction.retry_count >= 3 ? 'Exceeded' : 'Safe'}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-slate-500 block text-[11px]">High Value Threshold</span>
                <span className="font-bold text-white mt-0.5 block">₹{transaction.amount.toLocaleString('en-IN')}</span>
                <span className={transaction.amount >= 20000 ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                  {transaction.amount >= 20000 ? 'Requires Escalate' : '< ₹20k Safe'}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-slate-500 block text-[11px]">Fraud Flag</span>
                <span className="font-bold text-white mt-0.5 block">{transaction.failure_reason}</span>
                <span className={transaction.failure_reason === 'fraud_flag' ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                  {transaction.failure_reason === 'fraud_flag' ? 'Flagged' : 'Clean'}
                </span>
              </div>
            </div>
          </div>

          {/* Action Recommendation & Bounded Execution Control */}
          <div className="p-6 rounded-2xl glass-panel border border-emerald-500/30 bg-gradient-to-r from-indigo-950/40 to-slate-900 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Recommended Action</span>
              <div className="text-2xl font-black text-white mt-1">{analysis.recommended_action}</div>
              <p className="text-xs text-slate-300 mt-1">
                Executes bounded Razorpay sandbox test simulation.
              </p>
            </div>

            <button
              onClick={handleExecuteAction}
              disabled={executing || transaction.status === 'RECOVERED'}
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-extrabold text-xs shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 disabled:opacity-50 transition-all shrink-0"
            >
              {executing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Executing...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 fill-current" />
                  Execute {analysis.recommended_action}
                </>
              )}
            </button>
          </div>

          {/* Execution Result Feed */}
          {execResult && (
            <div className={`p-4 rounded-xl border flex items-center gap-3 ${execResult.success ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300' : 'bg-purple-950/40 border-purple-500/40 text-purple-300'}`}>
              <CheckCircle2 className="w-5 h-5 shrink-0" />
              <div className="text-xs">
                <div className="font-bold">{execResult.message}</div>
                <div className="font-mono text-[10px] mt-0.5 opacity-80">Razorpay Sim ID: {execResult.simulated_gateway_id}</div>
              </div>
            </div>
          )}

          {/* Audit Trail Timeline */}
          {transaction.audit_logs && transaction.audit_logs.length > 0 && (
            <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
              <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Clock className="w-4 h-4 text-indigo-400" />
                Audit Trail History
              </h3>
              <div className="space-y-3">
                {transaction.audit_logs.map((au) => (
                  <div key={au.id} className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-white">{au.decision}</span>
                      <span className="font-mono text-[10px] text-slate-500">
                        {new Date(au.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-slate-300">{au.reason}</p>
                    <div className="text-[11px] text-slate-400 pt-1">
                      Action Taken: <strong className="text-indigo-400">{au.action_taken}</strong> • Result: <strong className={au.execution_result === 'SUCCESS' ? 'text-emerald-400' : 'text-purple-400'}>{au.execution_result}</strong>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
