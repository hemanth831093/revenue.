import React, { useState } from 'react';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Transactions } from './pages/Transactions';
import { TransactionDetails } from './pages/TransactionDetails';
import { AIRecovery } from './pages/AIRecovery';
import { Analytics } from './pages/Analytics';
import { AuditLogs } from './pages/AuditLogs';
import { Settings } from './pages/Settings';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedTransactionId, setSelectedTransactionId] = useState<number | null>(null);

  const handleSelectTransaction = (id: number) => {
    setSelectedTransactionId(id);
    setActiveTab('transaction-detail');
  };

  const handleBackToTransactions = () => {
    setSelectedTransactionId(null);
    setActiveTab('transactions');
  };

  return (
    <Layout activeTab={activeTab} setActiveTab={(tab) => {
      setSelectedTransactionId(null);
      setActiveTab(tab);
    }}>
      {activeTab === 'dashboard' && (
        <Dashboard
          onNavigateToRecovery={() => setActiveTab('recovery')}
          onSelectTransaction={handleSelectTransaction}
        />
      )}

      {activeTab === 'transactions' && (
        <Transactions onSelectTransaction={handleSelectTransaction} />
      )}

      {activeTab === 'transaction-detail' && selectedTransactionId && (
        <TransactionDetails
          transactionId={selectedTransactionId}
          onBack={handleBackToTransactions}
        />
      )}

      {activeTab === 'recovery' && (
        <AIRecovery onSelectTransaction={handleSelectTransaction} />
      )}

      {activeTab === 'analytics' && <Analytics />}

      {activeTab === 'audit-logs' && <AuditLogs />}

      {activeTab === 'settings' && <Settings />}
    </Layout>
  );
};

export default App;
