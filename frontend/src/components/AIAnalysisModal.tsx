import React, { useState } from 'react';
import { Bot, ShieldCheck, Zap, AlertTriangle, CheckCircle2, XCircle, ArrowRight, RefreshCw, X } from 'lucide-react';
import { AIAnalysis } from '../types';
import { executeRecoveryAction } from '../services/api';
import { RiskBadge } from './RiskBadge';

interface Props {
  analysis: AIAnalysis;
  onClose: () => void;
  onSuccess: () => void;
}

export const AIAnalysisModal: React.FC<Props> = ({ analysis, onClose, onSuccess }) => {
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleExecute = async () => {
    setExecuting(true);
    try {
      const res = await executeRecoveryAction(analysis.transaction_id, analysis.recommended_action);
      setResult(res);
      onSuccess();
    } catch (e: any) {
      alert("Failed to execute recovery: " + (e.message || "Error"));
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-3xl shadow-2xl overflow-hidden glass-panel">
        {/* Header */}
        <div className="p-6 border-b border-slate-800/80 flex items-center justify-between bg-slate-900/60">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 glow-indigo">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                AI Payment Failure Diagnosis & Recovery
              </h2>
              <p className="text-xs text-slate-400 font-mono">Payment ID: {analysis.payment_id}</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
          {/* Recovery Probability & Priority Header */}
          <div className="p-5 rounded-2xl bg-slate-850 border border-slate-800 flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Recovery Probability</span>
              <div className="text-3xl font-extrabold text-white mt-1">
                {Math.round(analysis.recovery_probability * 100)}%
              </div>
              <span className="text-xs text-indigo-400">
                Expected Recoverable Value: ₹{analysis.expected_recovery_value.toLocaleString('en-IN')}
              </span>
            </div>
            <RiskBadge priority={analysis.priority} />
          </div>

          {/* AI Diagnosis */}
          <div className="space-y-2">
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              AI Failure Root-Cause Diagnosis
            </h3>
            <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/20">
              <div className="font-bold text-indigo-300 text-sm">{analysis.diagnosis}</div>
              <p className="text-xs text-slate-300 mt-1 leading-relaxed">{analysis.diagnosis_explanation}</p>
            </div>
          </div>

          {/* Risk Factors */}
          {analysis.risk_factors && analysis.risk_factors.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400">
                Evaluated Feature Signals
              </h3>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {analysis.risk_factors.map((rf, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                    <span>{rf}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Safety Rules Status */}
          <div className="space-y-2">
            <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Safety Bounded Controls Evaluated
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 flex flex-col">
                <span className="text-slate-400 text-[11px]">Max Retries Rule</span>
                <span className="font-semibold text-slate-200 mt-1">
                  {analysis.safety_checks.max_retries_rule?.current}/{analysis.safety_checks.max_retries_rule?.limit} retries
                </span>
                <span className={`text-[10px] font-bold mt-1 ${analysis.safety_checks.max_retries_rule?.triggered ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {analysis.safety_checks.max_retries_rule?.triggered ? 'Triggered (Escalate)' : 'Passed (Safe)'}
                </span>
              </div>

              <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 flex flex-col">
                <span className="text-slate-400 text-[11px]">High Value Threshold</span>
                <span className="font-semibold text-slate-200 mt-1">
                  ₹{analysis.amount.toLocaleString('en-IN')} / ₹{analysis.safety_checks.high_value_rule?.threshold.toLocaleString('en-IN')}
                </span>
                <span className={`text-[10px] font-bold mt-1 ${analysis.safety_checks.high_value_rule?.triggered ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {analysis.safety_checks.high_value_rule?.triggered ? 'Triggered (Escalate)' : 'Passed (Safe)'}
                </span>
              </div>

              <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 flex flex-col">
                <span className="text-slate-400 text-[11px]">Fraud Flag Check</span>
                <span className="font-semibold text-slate-200 mt-1">Velocity Filters</span>
                <span className={`text-[10px] font-bold mt-1 ${analysis.safety_checks.fraud_flag_rule?.triggered ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {analysis.safety_checks.fraud_flag_rule?.triggered ? 'Flagged' : 'Passed (Clean)'}
                </span>
              </div>
            </div>
          </div>

          {/* Recommended Action Card */}
          <div className="p-5 rounded-2xl bg-gradient-to-r from-indigo-900/40 to-emerald-900/30 border border-indigo-500/30 flex items-center justify-between">
            <div>
              <span className="text-xs font-extrabold uppercase tracking-wider text-indigo-300">Recommended Action</span>
              <div className="text-xl font-black text-white mt-0.5 flex items-center gap-2">
                {analysis.recommended_action}
              </div>
              <p className="text-xs text-slate-300 mt-1">
                {analysis.recommended_action === 'RETRY' && 'Execute instant simulated Razorpay test mandate retry.'}
                {analysis.recommended_action === 'PAYMENT_LINK' && 'Dispatch payment link to customer to update expired card.'}
                {analysis.recommended_action === 'REMINDER' && 'Send omnichannel reminder notification with instant payment trigger.'}
                {analysis.recommended_action === 'HUMAN_ESCALATION' && 'Escalate to merchant human operations team.'}
              </p>
            </div>
          </div>

          {/* Execution Result Banner */}
          {result && (
            <div className={`p-4 rounded-xl border flex items-center gap-3 ${result.success ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300' : 'bg-purple-950/40 border-purple-500/40 text-purple-300'}`}>
              {result.success ? <CheckCircle2 className="w-5 h-5 shrink-0" /> : <AlertTriangle className="w-5 h-5 shrink-0" />}
              <div className="text-xs">
                <div className="font-bold">{result.message}</div>
                <div className="font-mono text-[10px] mt-0.5 opacity-80">Gateway Sim ID: {result.simulated_gateway_id}</div>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-6 border-t border-slate-800/80 bg-slate-900/80 flex items-center justify-between">
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800"
          >
            Close
          </button>
          {!result ? (
            <button
              onClick={handleExecute}
              disabled={executing}
              className="px-6 py-2.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white shadow-lg shadow-indigo-600/30 flex items-center gap-2 transition-all disabled:opacity-50"
            >
              {executing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Executing Action...
                </>
              ) : (
                <>
                  <span>Execute {analysis.recommended_action}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          ) : (
            <button
              onClick={onClose}
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-slate-800 text-white hover:bg-slate-700"
            >
              Done
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
