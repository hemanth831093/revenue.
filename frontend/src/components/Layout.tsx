import React, { useState } from 'react';
import {
  LayoutDashboard,
  Receipt,
  Bot,
  BarChart3,
  FileCheck2,
  Settings,
  ShieldAlert,
  Sparkles,
  Zap,
  Activity,
  Menu,
  X
} from 'lucide-react';

interface Props {
  children: React.ReactNode;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Layout: React.FC<Props> = ({ children, activeTab, setActiveTab }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'transactions', label: 'Transactions', icon: Receipt },
    { id: 'recovery', label: 'AI Recovery', icon: Bot, badge: 'High Risk' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'audit-logs', label: 'Audit Logs', icon: FileCheck2 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen flex bg-slate-950 text-slate-100">
      {/* Sidebar Desktop */}
      <aside className="hidden lg:flex w-64 flex-col border-r border-slate-800/60 bg-slate-900/60 backdrop-blur-xl sticky top-0 h-screen z-20">
        <div className="p-6 border-b border-slate-800/60 flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-600 to-emerald-500 text-white shadow-lg shadow-indigo-500/20">
            <Zap className="w-6 h-6 fill-current" />
          </div>
          <div>
            <h1 className="text-xl font-black tracking-wider bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
              RecoverAI
            </h1>
            <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
              Autonomous Agent
            </span>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-4 py-3 rounded-xl text-sm font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-lg shadow-indigo-600/30 font-bold'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        <div className="p-4 m-4 rounded-xl glass-panel border border-slate-800/80 bg-slate-900/40">
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400">
            <Activity className="w-4 h-4 animate-pulse" />
            <span>Simulator Sandbox Active</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Razorpay Test Mode API Enabled</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className="h-16 border-b border-slate-800/60 bg-slate-900/40 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="lg:hidden p-2 text-slate-400 hover:text-white"
            >
              {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400 uppercase font-bold tracking-wider">Active Workspace</span>
              <span className="text-xs px-2.5 py-1 rounded-md bg-slate-800 font-mono text-indigo-300 border border-slate-700">
                Razorpay Merchant Sandbox
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 text-xs font-medium text-slate-300 px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Scikit-learn + LLM Risk Scoring Engine v1.0</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white shadow-md">
              AI
            </div>
          </div>
        </header>

        {/* Page Container */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
};
