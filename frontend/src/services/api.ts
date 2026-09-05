import axios from 'axios';
import { Transaction, DashboardMetrics, AIAnalysis, AuditLog, AppSettings } from '../types';

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const getDashboardMetrics = async (): Promise<DashboardMetrics> => {
  const res = await api.get('/api/dashboard');
  return res.data;
};

export const getTransactions = async (params: {
  search?: string;
  status?: string;
  failure_reason?: string;
  priority?: string;
  min_amount?: number;
  max_amount?: number;
  page?: number;
  limit?: number;
}) => {
  const res = await api.get('/api/transactions', { params });
  return res.data;
};

export const getTransactionDetail = async (id: number): Promise<Transaction> => {
  const res = await api.get(`/api/transactions/${id}`);
  return res.data;
};

export const analyzeTransaction = async (id: number): Promise<AIAnalysis> => {
  const res = await api.post(`/api/ai/analyze/${id}`);
  return res.data;
};

export const executeRecoveryAction = async (id: number, action_type?: string) => {
  const res = await api.post(`/api/recovery/execute/${id}`, { action_type });
  return res.data;
};

export const batchExecuteRecovery = async (transaction_ids: number[]) => {
  const res = await api.post('/api/recovery/batch-execute', transaction_ids);
  return res.data;
};

export const getAuditLogs = async (params: {
  search?: string;
  action_type?: string;
  page?: number;
  limit?: number;
}) => {
  const res = await api.get('/api/audit-logs', { params });
  return res.data;
};

export const getSettings = async (): Promise<AppSettings> => {
  const res = await api.get('/api/settings');
  return res.data;
};

export const updateSettings = async (settings: Partial<AppSettings>): Promise<AppSettings> => {
  const res = await api.put('/api/settings', settings);
  return res.data;
};
