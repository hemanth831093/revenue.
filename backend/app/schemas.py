from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

# Transaction Schemas
class TransactionBase(BaseModel):
    payment_id: str
    customer_id: str
    customer_name: str
    customer_email: str
    amount: float
    payment_method: str
    failure_reason: str
    failure_code: Optional[str] = None
    previous_successes: int = 0
    previous_failures: int = 0
    retry_count: int = 0

class TransactionCreate(TransactionBase):
    status: Optional[str] = "FAILED"

class TransactionRead(TransactionBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Risk Score Schemas
class RiskScoreRead(BaseModel):
    id: int
    transaction_id: int
    recovery_probability: float
    priority: str
    risk_factors: Optional[str] = None
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True

# Recovery Action Schemas
class RecoveryActionRead(BaseModel):
    id: int
    transaction_id: int
    action_type: str
    status: str
    amount_recovered: float
    razorpay_sim_id: Optional[str] = None
    executed_at: datetime
    response_metadata: Optional[str] = None

    class Config:
        from_attributes = True

# Audit Log Schemas
class AuditLogRead(BaseModel):
    id: int
    transaction_id: int
    decision: str
    reason: str
    action_taken: str
    execution_result: str
    stopping_rules_applied: Optional[str] = None
    created_at: datetime
    
    # Nested info optional
    payment_id: Optional[str] = None
    customer_name: Optional[str] = None
    amount: Optional[float] = None

    class Config:
        from_attributes = True

# AI Analysis Response Schema
class AIAnalysisResponse(BaseModel):
    transaction_id: int
    payment_id: Optional[str] = None
    amount: Optional[float] = None
    diagnosis: str
    diagnosis_explanation: Optional[str] = None
    root_cause: Optional[str] = None
    recovery_probability: float
    priority: str
    recommended_action: str
    reason: str
    expected_recovery_value: float
    risk_factors: Optional[List[str]] = None
    safety_checks: Dict[str, Any]
    stopping_rules_applied: List[str] = []

# Action Execution Request & Response
class ExecuteActionRequest(BaseModel):
    action_type: Optional[str] = None  # RETRY, PAYMENT_LINK, REMINDER, HUMAN_ESCALATION (If omitted, uses recommended_action)

class ExecuteActionResponse(BaseModel):
    success: bool
    message: str
    action_id: int
    action_type: str
    simulated_gateway_id: str
    amount_recovered: float
    new_status: str
    audit_log_id: int

# Dashboard Metrics Schema
class DashboardMetrics(BaseModel):
    total_revenue_at_risk: float
    total_revenue_recovered: float
    failed_payments_count: int
    recovered_payments_count: int
    recovery_rate: float
    high_priority_count: int
    recent_actions: List[Dict[str, Any]]
    chart_revenue_data: List[Dict[str, Any]]
    chart_reason_data: List[Dict[str, Any]]

# App Settings Schema
class SettingsResponse(BaseModel):
    max_retries: int
    human_escalation_threshold: float
    test_mode: bool
    razorpay_configured: bool
    llm_configured: bool

class SettingsUpdate(BaseModel):
    max_retries: Optional[int] = None
    human_escalation_threshold: Optional[float] = None
    test_mode: Optional[bool] = None
