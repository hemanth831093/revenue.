export interface Transaction {
  id: number;
  payment_id: string;
  customer_id: string;
  customer_name: string;
  customer_email: string;
  amount: number;
  payment_method: 'UPI' | 'Credit Card' | 'Debit Card' | 'Netbanking' | string;
  status: 'FAILED' | 'RECOVERED' | 'IN_PROGRESS' | 'ESCALATED' | string;
  failure_reason: 'bank_timeout' | 'insufficient_funds' | 'card_expired' | 'network_error' | 'fraud_flag' | string;
  failure_code?: string;
  previous_successes: number;
  previous_failures: number;
  retry_count: number;
  recovery_probability?: number;
  priority?: 'HIGH' | 'MEDIUM' | 'LOW' | string;
  risk_factors?: string[];
  created_at: string;
  recovery_actions?: RecoveryAction[];
  audit_logs?: AuditLog[];
}

export interface RecoveryAction {
  id: number;
  transaction_id: number;
  action_type: 'RETRY' | 'PAYMENT_LINK' | 'REMINDER' | 'HUMAN_ESCALATION' | string;
  status: 'PENDING' | 'SUCCESS' | 'FAILED' | 'ESCALATED' | string;
  amount_recovered: number;
  razorpay_sim_id?: string;
  executed_at: string;
}

export interface AuditLog {
  id: number;
  transaction_id: number;
  payment_id?: string;
  customer_name?: string;
  amount?: number;
  decision: string;
  reason: string;
  action_taken: string;
  execution_result: string;
  stopping_rules_applied?: Record<string, any>;
  created_at: string;
}

export interface AIAnalysis {
  transaction_id: number;
  payment_id: string;
  amount: number;
  recovery_probability: number;
  priority: 'HIGH' | 'MEDIUM' | 'LOW' | string;
  diagnosis: string;
  diagnosis_explanation: string;
  recommended_action: 'RETRY' | 'PAYMENT_LINK' | 'REMINDER' | 'HUMAN_ESCALATION' | string;
  expected_recovery_value: number;
  risk_factors: string[];
  safety_checks: Record<string, any>;
}

export interface DashboardMetrics {
  total_revenue_at_risk: number;
  total_revenue_recovered: number;
  failed_payments_count: number;
  recovered_payments_count: number;
  escalated_payments_count: number;
  recovery_rate: number;
  high_priority_count: number;
  recent_actions: Array<{
    id: number;
    transaction_id: number;
    payment_id: string;
    customer_name: string;
    amount: number;
    action_taken: string;
    execution_result: string;
    created_at: string;
  }>;
  chart_revenue_data: Array<{ category: string; amount: number }>;
  chart_reason_data: Array<{ reason: string; count: number }>;
}

export interface AppSettings {
  max_retries: number;
  human_escalation_threshold: number;
  test_mode: boolean;
  razorpay_configured: boolean;
  llm_configured: boolean;
}
