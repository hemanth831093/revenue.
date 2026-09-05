import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, ShieldCheck, Save, RefreshCw, CheckCircle2, Zap } from 'lucide-react';
import { getSettings, updateSettings } from '../services/api';
import { AppSettings } from '../types';

export const Settings: React.FC = () => {
  const [settings, setSettingsData] = useState<AppSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState(false);

  // Form states
  const [maxRetries, setMaxRetries] = useState(3);
  const [threshold, setThreshold] = useState(20000);
  const [testMode, setTestMode] = useState(true);

  useEffect(() => {
    getSettings().then((data) => {
      setSettingsData(data);
      setMaxRetries(data.max_retries);
      setThreshold(data.human_escalation_threshold);
      setTestMode(data.test_mode);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await updateSettings({
        max_retries: maxRetries,
        human_escalation_threshold: threshold,
        test_mode: testMode
      });
      setSettingsData(updated);
      setSuccessMsg(true);
      setTimeout(() => setSuccessMsg(false), 3000);
    } catch (e) {
      alert("Failed to save settings.");
    } finally {
      setSaving(false);
    }
  };

  if (loading || !settings) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <RefreshCw className="w-8 h-8 text-indigo-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-2xl font-black text-white flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-indigo-400" />
          Autonomous Agent Safety & Rule Settings
        </h1>
        <p className="text-xs text-slate-400">Configure hard stopping boundaries, financial threshold limits, and simulator sandbox settings</p>
      </div>

      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          Settings updated successfully! Safety rules applied immediately to all payment evaluations.
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Safety Rules Section */}
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-6">
          <h2 className="text-base font-extrabold text-white flex items-center gap-2 border-b border-slate-800/80 pb-3">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Safety Stopping Boundaries
          </h2>

          <div className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Maximum Retry Count Limit (<code className="text-indigo-300 font-mono">MAX_RETRIES</code>)
              </label>
              <input
                type="number"
                min={1}
                max={10}
                value={maxRetries}
                onChange={(e) => setMaxRetries(Number(e.target.value))}
                className="w-full sm:w-64 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white font-mono focus:outline-none focus:border-indigo-500"
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Transactions reaching this retry limit will automatically halt automated retries and trigger <strong className="text-slate-300">HUMAN_ESCALATION</strong>.
              </p>
            </div>

            <div>
              <label className="block text-slate-300 font-bold mb-1">
                Human Escalation Amount Threshold (<code className="text-indigo-300 font-mono">HUMAN_ESCALATION_THRESHOLD</code> in ₹)
              </label>
              <input
                type="number"
                step={500}
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
                className="w-full sm:w-64 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white font-mono focus:outline-none focus:border-indigo-500"
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Any failed payment $\ge$ ₹{threshold.toLocaleString('en-IN')} requires explicit merchant human review.
              </p>
            </div>

            <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
              <div>
                <span className="block text-white font-bold">Simulator Test Mode</span>
                <span className="text-[11px] text-slate-500">
                  Operate in Razorpay sandbox test mode with simulated gateway responses.
                </span>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={testMode}
                  onChange={(e) => setTestMode(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Integration Status Section */}
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4 text-xs">
          <h2 className="text-base font-extrabold text-white flex items-center gap-2 border-b border-slate-800/80 pb-3">
            <Zap className="w-5 h-5 text-indigo-400" />
            Integrations & API Gateways
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <div className="flex justify-between">
                <span className="font-bold text-white">Razorpay Test Gateway</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {settings.razorpay_configured ? 'Active' : 'Sandbox Fallback'}
                </span>
              </div>
              <p className="text-slate-400 text-[11px]">Razorpay Test API Keys configured in environment.</p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <div className="flex justify-between">
                <span className="font-bold text-white">Scikit-learn + LLM Engine</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  Active (Local ML)
                </span>
              </div>
              <p className="text-slate-400 text-[11px]">Transparent Scikit-learn Risk Model + Rule AI Engine active.</p>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 text-white font-extrabold text-xs shadow-lg shadow-indigo-600/30 flex items-center gap-2 transition-all disabled:opacity-50"
        >
          {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
          <span>Save Safety Configurations</span>
        </button>
      </form>
    </div>
  );
};
